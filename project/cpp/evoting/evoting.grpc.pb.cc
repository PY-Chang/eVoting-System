// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: evoting.proto

#include "evoting.pb.h"
#include "evoting.grpc.pb.h"

#include <functional>
#include <grpcpp/impl/codegen/async_stream.h>
#include <grpcpp/impl/codegen/async_unary_call.h>
#include <grpcpp/impl/codegen/channel_interface.h>
#include <grpcpp/impl/codegen/client_unary_call.h>
#include <grpcpp/impl/codegen/client_callback.h>
#include <grpcpp/impl/codegen/message_allocator.h>
#include <grpcpp/impl/codegen/method_handler.h>
#include <grpcpp/impl/codegen/rpc_service_method.h>
#include <grpcpp/impl/codegen/server_callback.h>
#include <grpcpp/impl/codegen/server_callback_handlers.h>
#include <grpcpp/impl/codegen/server_context.h>
#include <grpcpp/impl/codegen/service_type.h>
#include <grpcpp/impl/codegen/sync_stream.h>
namespace voting {

static const char* eVoting_method_names[] = {
  "/voting.eVoting/PreAuth",
  "/voting.eVoting/Auth",
  "/voting.eVoting/CreateElection",
  "/voting.eVoting/CastVote",
  "/voting.eVoting/GetResult",
};

std::unique_ptr< eVoting::Stub> eVoting::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  (void)options;
  std::unique_ptr< eVoting::Stub> stub(new eVoting::Stub(channel, options));
  return stub;
}

eVoting::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options)
  : channel_(channel), rpcmethod_PreAuth_(eVoting_method_names[0], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_Auth_(eVoting_method_names[1], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_CreateElection_(eVoting_method_names[2], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_CastVote_(eVoting_method_names[3], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_GetResult_(eVoting_method_names[4], options.suffix_for_stats(),::grpc::internal::RpcMethod::NORMAL_RPC, channel)
  {}

::grpc::Status eVoting::Stub::PreAuth(::grpc::ClientContext* context, const ::voting::VoterName& request, ::voting::Challenge* response) {
  return ::grpc::internal::BlockingUnaryCall< ::voting::VoterName, ::voting::Challenge, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_PreAuth_, context, request, response);
}

void eVoting::Stub::async::PreAuth(::grpc::ClientContext* context, const ::voting::VoterName* request, ::voting::Challenge* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::voting::VoterName, ::voting::Challenge, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_PreAuth_, context, request, response, std::move(f));
}

void eVoting::Stub::async::PreAuth(::grpc::ClientContext* context, const ::voting::VoterName* request, ::voting::Challenge* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_PreAuth_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::voting::Challenge>* eVoting::Stub::PrepareAsyncPreAuthRaw(::grpc::ClientContext* context, const ::voting::VoterName& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::voting::Challenge, ::voting::VoterName, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_PreAuth_, context, request);
}

::grpc::ClientAsyncResponseReader< ::voting::Challenge>* eVoting::Stub::AsyncPreAuthRaw(::grpc::ClientContext* context, const ::voting::VoterName& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncPreAuthRaw(context, request, cq);
  result->StartCall();
  return result;
}

::grpc::Status eVoting::Stub::Auth(::grpc::ClientContext* context, const ::voting::AuthRequest& request, ::voting::AuthToken* response) {
  return ::grpc::internal::BlockingUnaryCall< ::voting::AuthRequest, ::voting::AuthToken, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_Auth_, context, request, response);
}

void eVoting::Stub::async::Auth(::grpc::ClientContext* context, const ::voting::AuthRequest* request, ::voting::AuthToken* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::voting::AuthRequest, ::voting::AuthToken, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_Auth_, context, request, response, std::move(f));
}

void eVoting::Stub::async::Auth(::grpc::ClientContext* context, const ::voting::AuthRequest* request, ::voting::AuthToken* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_Auth_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::voting::AuthToken>* eVoting::Stub::PrepareAsyncAuthRaw(::grpc::ClientContext* context, const ::voting::AuthRequest& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::voting::AuthToken, ::voting::AuthRequest, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_Auth_, context, request);
}

::grpc::ClientAsyncResponseReader< ::voting::AuthToken>* eVoting::Stub::AsyncAuthRaw(::grpc::ClientContext* context, const ::voting::AuthRequest& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncAuthRaw(context, request, cq);
  result->StartCall();
  return result;
}

::grpc::Status eVoting::Stub::CreateElection(::grpc::ClientContext* context, const ::voting::Election& request, ::voting::ElectionStatus* response) {
  return ::grpc::internal::BlockingUnaryCall< ::voting::Election, ::voting::ElectionStatus, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_CreateElection_, context, request, response);
}

void eVoting::Stub::async::CreateElection(::grpc::ClientContext* context, const ::voting::Election* request, ::voting::ElectionStatus* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::voting::Election, ::voting::ElectionStatus, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_CreateElection_, context, request, response, std::move(f));
}

void eVoting::Stub::async::CreateElection(::grpc::ClientContext* context, const ::voting::Election* request, ::voting::ElectionStatus* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_CreateElection_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::voting::ElectionStatus>* eVoting::Stub::PrepareAsyncCreateElectionRaw(::grpc::ClientContext* context, const ::voting::Election& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::voting::ElectionStatus, ::voting::Election, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_CreateElection_, context, request);
}

::grpc::ClientAsyncResponseReader< ::voting::ElectionStatus>* eVoting::Stub::AsyncCreateElectionRaw(::grpc::ClientContext* context, const ::voting::Election& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncCreateElectionRaw(context, request, cq);
  result->StartCall();
  return result;
}

::grpc::Status eVoting::Stub::CastVote(::grpc::ClientContext* context, const ::voting::Vote& request, ::voting::VoteStatus* response) {
  return ::grpc::internal::BlockingUnaryCall< ::voting::Vote, ::voting::VoteStatus, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_CastVote_, context, request, response);
}

void eVoting::Stub::async::CastVote(::grpc::ClientContext* context, const ::voting::Vote* request, ::voting::VoteStatus* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::voting::Vote, ::voting::VoteStatus, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_CastVote_, context, request, response, std::move(f));
}

void eVoting::Stub::async::CastVote(::grpc::ClientContext* context, const ::voting::Vote* request, ::voting::VoteStatus* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_CastVote_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::voting::VoteStatus>* eVoting::Stub::PrepareAsyncCastVoteRaw(::grpc::ClientContext* context, const ::voting::Vote& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::voting::VoteStatus, ::voting::Vote, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_CastVote_, context, request);
}

::grpc::ClientAsyncResponseReader< ::voting::VoteStatus>* eVoting::Stub::AsyncCastVoteRaw(::grpc::ClientContext* context, const ::voting::Vote& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncCastVoteRaw(context, request, cq);
  result->StartCall();
  return result;
}

::grpc::Status eVoting::Stub::GetResult(::grpc::ClientContext* context, const ::voting::ElectionName& request, ::voting::ElectionResult* response) {
  return ::grpc::internal::BlockingUnaryCall< ::voting::ElectionName, ::voting::ElectionResult, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), rpcmethod_GetResult_, context, request, response);
}

void eVoting::Stub::async::GetResult(::grpc::ClientContext* context, const ::voting::ElectionName* request, ::voting::ElectionResult* response, std::function<void(::grpc::Status)> f) {
  ::grpc::internal::CallbackUnaryCall< ::voting::ElectionName, ::voting::ElectionResult, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_GetResult_, context, request, response, std::move(f));
}

void eVoting::Stub::async::GetResult(::grpc::ClientContext* context, const ::voting::ElectionName* request, ::voting::ElectionResult* response, ::grpc::ClientUnaryReactor* reactor) {
  ::grpc::internal::ClientCallbackUnaryFactory::Create< ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(stub_->channel_.get(), stub_->rpcmethod_GetResult_, context, request, response, reactor);
}

::grpc::ClientAsyncResponseReader< ::voting::ElectionResult>* eVoting::Stub::PrepareAsyncGetResultRaw(::grpc::ClientContext* context, const ::voting::ElectionName& request, ::grpc::CompletionQueue* cq) {
  return ::grpc::internal::ClientAsyncResponseReaderHelper::Create< ::voting::ElectionResult, ::voting::ElectionName, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(channel_.get(), cq, rpcmethod_GetResult_, context, request);
}

::grpc::ClientAsyncResponseReader< ::voting::ElectionResult>* eVoting::Stub::AsyncGetResultRaw(::grpc::ClientContext* context, const ::voting::ElectionName& request, ::grpc::CompletionQueue* cq) {
  auto* result =
    this->PrepareAsyncGetResultRaw(context, request, cq);
  result->StartCall();
  return result;
}

eVoting::Service::Service() {
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      eVoting_method_names[0],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< eVoting::Service, ::voting::VoterName, ::voting::Challenge, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](eVoting::Service* service,
             ::grpc::ServerContext* ctx,
             const ::voting::VoterName* req,
             ::voting::Challenge* resp) {
               return service->PreAuth(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      eVoting_method_names[1],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< eVoting::Service, ::voting::AuthRequest, ::voting::AuthToken, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](eVoting::Service* service,
             ::grpc::ServerContext* ctx,
             const ::voting::AuthRequest* req,
             ::voting::AuthToken* resp) {
               return service->Auth(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      eVoting_method_names[2],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< eVoting::Service, ::voting::Election, ::voting::ElectionStatus, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](eVoting::Service* service,
             ::grpc::ServerContext* ctx,
             const ::voting::Election* req,
             ::voting::ElectionStatus* resp) {
               return service->CreateElection(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      eVoting_method_names[3],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< eVoting::Service, ::voting::Vote, ::voting::VoteStatus, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](eVoting::Service* service,
             ::grpc::ServerContext* ctx,
             const ::voting::Vote* req,
             ::voting::VoteStatus* resp) {
               return service->CastVote(ctx, req, resp);
             }, this)));
  AddMethod(new ::grpc::internal::RpcServiceMethod(
      eVoting_method_names[4],
      ::grpc::internal::RpcMethod::NORMAL_RPC,
      new ::grpc::internal::RpcMethodHandler< eVoting::Service, ::voting::ElectionName, ::voting::ElectionResult, ::grpc::protobuf::MessageLite, ::grpc::protobuf::MessageLite>(
          [](eVoting::Service* service,
             ::grpc::ServerContext* ctx,
             const ::voting::ElectionName* req,
             ::voting::ElectionResult* resp) {
               return service->GetResult(ctx, req, resp);
             }, this)));
}

eVoting::Service::~Service() {
}

::grpc::Status eVoting::Service::PreAuth(::grpc::ServerContext* context, const ::voting::VoterName* request, ::voting::Challenge* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status eVoting::Service::Auth(::grpc::ServerContext* context, const ::voting::AuthRequest* request, ::voting::AuthToken* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status eVoting::Service::CreateElection(::grpc::ServerContext* context, const ::voting::Election* request, ::voting::ElectionStatus* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status eVoting::Service::CastVote(::grpc::ServerContext* context, const ::voting::Vote* request, ::voting::VoteStatus* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status eVoting::Service::GetResult(::grpc::ServerContext* context, const ::voting::ElectionName* request, ::voting::ElectionResult* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


}  // namespace voting
