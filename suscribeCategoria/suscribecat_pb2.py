# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: suscribecat.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'suscribecat.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11suscribecat.proto\x12\x10suscribcategoria\"?\n\rClientRequest\x12\x0e\n\x06\x63lient\x18\x01 \x01(\x05\x12\r\n\x05passw\x18\x02 \x01(\t\x12\x0f\n\x07seccion\x18\x03 \x01(\t\"\x1c\n\x08Response\x12\x10\n\x08response\x18\x01 \x01(\t2^\n\x08Suscribe\x12R\n\x11SuscribeCategoria\x12\x1f.suscribcategoria.ClientRequest\x1a\x1a.suscribcategoria.Response\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suscribecat_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CLIENTREQUEST']._serialized_start=39
  _globals['_CLIENTREQUEST']._serialized_end=102
  _globals['_RESPONSE']._serialized_start=104
  _globals['_RESPONSE']._serialized_end=132
  _globals['_SUSCRIBE']._serialized_start=134
  _globals['_SUSCRIBE']._serialized_end=228
# @@protoc_insertion_point(module_scope)
