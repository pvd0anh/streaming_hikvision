/**
 * @fileoverview gRPC-Web generated client stub for 
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!



const grpc = {};
grpc.web = require('grpc-web');

const proto = require('./dl_server_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.DLServerClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.DLServerPromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.DLImageTaskRequest,
 *   !proto.DLImageTaskReply>}
 */
const methodDescriptor_DLServer_proceed_image_task = new grpc.web.MethodDescriptor(
  '/DLServer/proceed_image_task',
  grpc.web.MethodType.UNARY,
  proto.DLImageTaskRequest,
  proto.DLImageTaskReply,
  /** @param {!proto.DLImageTaskRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.DLImageTaskReply.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.DLImageTaskRequest,
 *   !proto.DLImageTaskReply>}
 */
const methodInfo_DLServer_proceed_image_task = new grpc.web.AbstractClientBase.MethodInfo(
  proto.DLImageTaskReply,
  /** @param {!proto.DLImageTaskRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.DLImageTaskReply.deserializeBinary
);


/**
 * @param {!proto.DLImageTaskRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.DLImageTaskReply)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.DLImageTaskReply>|undefined}
 *     The XHR Node Readable Stream
 */
proto.DLServerClient.prototype.proceed_image_task =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/DLServer/proceed_image_task',
      request,
      metadata || {},
      methodDescriptor_DLServer_proceed_image_task,
      callback);
};


/**
 * @param {!proto.DLImageTaskRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.DLImageTaskReply>}
 *     A native promise that resolves to the response
 */
proto.DLServerPromiseClient.prototype.proceed_image_task =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/DLServer/proceed_image_task',
      request,
      metadata || {},
      methodDescriptor_DLServer_proceed_image_task);
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.DLVideoTaskRequest,
 *   !proto.DLVideoTaskReply>}
 */
const methodDescriptor_DLServer_proceed_video_task = new grpc.web.MethodDescriptor(
  '/DLServer/proceed_video_task',
  grpc.web.MethodType.UNARY,
  proto.DLVideoTaskRequest,
  proto.DLVideoTaskReply,
  /** @param {!proto.DLVideoTaskRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.DLVideoTaskReply.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.DLVideoTaskRequest,
 *   !proto.DLVideoTaskReply>}
 */
const methodInfo_DLServer_proceed_video_task = new grpc.web.AbstractClientBase.MethodInfo(
  proto.DLVideoTaskReply,
  /** @param {!proto.DLVideoTaskRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.DLVideoTaskReply.deserializeBinary
);


/**
 * @param {!proto.DLVideoTaskRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.DLVideoTaskReply)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.DLVideoTaskReply>|undefined}
 *     The XHR Node Readable Stream
 */
proto.DLServerClient.prototype.proceed_video_task =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/DLServer/proceed_video_task',
      request,
      metadata || {},
      methodDescriptor_DLServer_proceed_video_task,
      callback);
};


/**
 * @param {!proto.DLVideoTaskRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.DLVideoTaskReply>}
 *     A native promise that resolves to the response
 */
proto.DLServerPromiseClient.prototype.proceed_video_task =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/DLServer/proceed_video_task',
      request,
      metadata || {},
      methodDescriptor_DLServer_proceed_video_task);
};


module.exports = proto;

