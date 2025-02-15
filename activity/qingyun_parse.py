import json
import struct
import base64
from enum import Enum
from typing import List, Dict

from google.protobuf.json_format import MessageToDict, ParseDict
import common.utils as utils
from liqi_proto import liqi_pb2 as pb

from common.log_helper import LOGGER

keys = [0x84, 0x5e, 0x4e, 0x42, 0x39, 0xa2, 0x1f, 0x60, 0x1c]


class MsgType(Enum):
    """ Majsoul websocket message type"""
    NOTIFY = 1
    """ Server to client notification, 0x01+protobuf """
    REQ = 2
    """ Client to server request, 0x02 + msg_id(2 bytes) + protobuf"""
    RES = 3
    """ Server to client response, 0x03 + msg_id(2 bytes) + protobuf"""

    def __repr__(self):
        return f"{self.name}({self.value})"


def decode(data: bytes):
    data = bytearray(data)
    for i in range(len(data)):
        u = (23 ^ len(data)) + 5 * i + keys[i % len(keys)] & 255
        data[i] ^= u
    return bytes(data)


def parseVarint(buf, p):
    # parse a varint from protobuf
    data = 0
    base = 0
    while p < len(buf):
        data += (buf[p] & 127) << base
        base += 7
        p += 1
        if buf[p - 1] >> 7 == 0:
            break
    return data, p


def fromProtobuf(buf) -> List[Dict]:
    # """
    # dump the struct of protobuf
    # buf: protobuf bytes
    # """
    p = 0
    result = []
    while p < len(buf):
        block_begin = p
        block_type = (buf[p] & 7)
        block_id = buf[p] >> 3
        p += 1
        if block_type == 0:
            # varint
            block_type = 'varint'
            data, p = parseVarint(buf, p)
        elif block_type == 2:
            # string
            block_type = 'string'
            s_len, p = parseVarint(buf, p)
            data = buf[p:p + s_len]
            p += s_len
        else:
            raise ValueError(f"Unknown type: {block_type}, at {p}")
        result.append({'id': block_id, 'type': block_type,
                       'data': data, 'begin': block_begin})
    return result


def parse(self, flow_msg) -> dict | None:
    # parse一帧WS flow msg，要求按顺序parse
    if isinstance(flow_msg, bytes):
        buf = flow_msg
    else:
        buf = flow_msg.content
        # from_client = flow_msg.from_client
    result = dict()
    msg_type = MsgType(buf[0])  # 通信报文类型
    if msg_type == MsgType.NOTIFY:
        msg_block = fromProtobuf(buf[1:])  # 解析剩余报文结构
        method_name = msg_block[0]['data'].decode()

        # msg_block结构通常为
        # [{'id': 1, 'type': 'string', 'data': b'.lq.ActionPrototype'},
        # {'id': 2, 'type': 'string','data': b'protobuf_bytes'}]

        _, lq, message_name = method_name.split('.')
        liqi_pb2_notify = getattr(pb, message_name)
        proto_obj = liqi_pb2_notify.FromString(msg_block[1]['data'])
        dict_obj = MessageToDict(proto_obj, always_print_fields_with_no_presence=True)
        if 'data' in dict_obj:
            B = base64.b64decode(dict_obj['data'])
            action_proto_obj = getattr(pb, dict_obj['name']).FromString(decode(B))
            action_dict_obj = MessageToDict(action_proto_obj, always_print_fields_with_no_presence=True)
            dict_obj['data'] = action_dict_obj
        msg_id = -1
    else:
        msg_id = struct.unpack('<H', buf[1:3])[0]  # 小端序解析报文编号(0~255)
        msg_block = fromProtobuf(buf[3:])  # 解析剩余报文结构
        # """
        #     msg_block结构通常为
        #     [{'id': 1, 'type': 'string', 'data': b'.lq.FastTest.authGame'},
        #     {'id': 2, 'type': 'string','data': b'protobuf_bytes'}]
        # """
        if msg_type == MsgType.REQ:
            assert (msg_id < 1 << 16)
            assert (len(msg_block) == 2)
            # assert(msg_id not in self.res_type)
            method_name = msg_block[0]['data'].decode()
            _, lq, service, rpc = method_name.split('.')
            proto_domain = self.jsonProto['nested'][lq]['nested'][service]['methods'][rpc]
            liqi_pb2_req = getattr(pb, proto_domain['requestType'])
            proto_obj = liqi_pb2_req.FromString(msg_block[1]['data'])
            dict_obj = MessageToDict(proto_obj, always_print_fields_with_no_presence=True)
            self.res_type[msg_id] = (method_name, getattr(
                pb, proto_domain['responseType']))
            self.msg_id = msg_id
        elif msg_type == MsgType.RES:
            assert (len(msg_block[0]['data']) == 0)
            assert (msg_id in self.res_type)
            method_name, liqi_pb2_res = self.res_type.pop(msg_id)
            proto_obj = liqi_pb2_res.FromString(msg_block[1]['data'])
            dict_obj = MessageToDict(proto_obj, always_print_fields_with_no_presence=True)
        else:
            LOGGER.error('unknow msg (type=%s): %s', msg_type, buf)
            return None
    result = {'id': msg_id, 'type': msg_type,
              'method': method_name, 'data': dict_obj}
    self.tot += 1
    return result


def qingyun_modify(message: str) -> str:
    pass
