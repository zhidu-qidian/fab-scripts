# coding: utf-8

import os.path
import time
from fabric.api import run, env, roles, cd

env.parallel = True
env.use_ssh_config = True
env.hosts = [
    "node3", "node4", "node5",
    "node110",
    "a1", "a2", "a4",
    "t1", "t2", "t3"
]
M = {
    1: "pipeline-atlas-image",
    2: "pipeline-atlas-upload",
    3: "pipeline-comment-upload",
    4: "pipeline-comments",
    5: "pipeline-download",
    6: "pipeline-es-insert",
    7: "pipeline-judge",
    8: "pipeline-judge-download",
    9: "pipeline-news-image",
    10: "pipeline-news-upload",
    11: "pipeline-offline-process",
    12: "pipeline-parse-article",
    13: "pipeline-parse-list",
    14: "pipeline-publish-name",
    15: "pipeline-third-party",
    16: "pipeline-relate-news",
    17: "spider-baidu",
    18: "spider-haowai",
    19: "thirdparty",
}
env.roledefs = {
    "pipeline": ["node3", "node4", "node5", "node110", "a1", "a2", "a4"],
    "swarm-nodes": ["t1", "t2", "t3"],
    "swarm-server": ["t1"],
    "wechat": ["node3", "node4", "node5", "a1", "a2", "a4"],

    M[1]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[2]: ["node110", "node3", "node4", "node5"],
    M[3]: ["node110", "node3", "node4", "node5"],
    M[4]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[5]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[6]: ["node110", "node3", "node4", "node5"],
    M[7]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[8]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[9]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[10]: ["node3", "node4", "node5"],
    M[11]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[12]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[13]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[14]: ["node110", "node3", "node4", "node5"],
    M[15]: ["node110", "node3", "node4", "node5", "a1", "a2", "a4"],
    M[16]: ["node3", "node4", "node5"],
    M[17]: ["node3"],
    M[18]: ["node3"],
    M[19]: ["node3", "node4", "node5"],
}


COMMANDS = {"start", "stop", "restart", "status"}


@roles("pipeline")
def pull_spider_code():
    """pull spider code to all hosts"""
    with cd("~/github/spider-pipeline"):
        run("git pull")


@roles("wechat")
def pull_wechat_code():
    """pull wechat code to all hosts"""
    with cd("~/github/browser-spiders/"):
        run("git pull")


@roles("swarm-nodes")
def pull_parser_code(service=None):
    """拉取解析服务相关代码, 参数:service=None,表示所有;可取值:article-parser,judge-page,list-parser,service-api"""
    if service is None:
        for p in DOCKER_PROJECTS:
            _pull_parser_service(p)
    else:
        _pull_parser_service(service)


@roles("pipeline")
def command(cmd):
    """部署 pipeline 的机器在 shell 执行命令

    :param cmd: shell 要执行的指令
    :type cmd: str
    """
    run(cmd)


def _supervisor_pipeline(pipeline, command):
    project = pipeline + ":*"
    run("supervisorctl %s %s" % (command, project))


@roles(M[1])
def pipeline_atlas_image(cmd):
    """通过 supervisorctl 命令管理该任务, cmd:start, stop, restart, status"""
    assert cmd in COMMANDS
    _supervisor_pipeline(M[1], cmd)


@roles(M[2])
def pipeline_atlas_upload(cmd):
    """通过 supervisorctl 命令管理该任务, cmd:start, stop, restart, status"""
    assert cmd in COMMANDS
    _supervisor_pipeline(M[2], cmd)


@roles(M[3])
def pipeline_comment_upload(cmd):
    """通过 supervisorctl 命令管理该任务, cmd:start, stop, restart, status"""
    assert cmd in COMMANDS
    _supervisor_pipeline(M[3], cmd)


@roles(M[4])
def pipeline_comments(cmd):
    """通过 supervisorctl 命令管理该任务, cmd:start, stop, restart, status"""
    assert cmd in COMMANDS
    _supervisor_pipeline(M[4], cmd)


@roles(M[5])
def pipeline_download(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[5], cmd)


@roles(M[6])
def pipeline_es_insert(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[6], cmd)


@roles(M[7])
def pipeline_judge(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[7], cmd)


@roles(M[8])
def pipeline_judge_download(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[8], cmd)


@roles(M[9])
def pipeline_news_image(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[9], cmd)


@roles(M[10])
def pipeline_news_upload(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[10], cmd)


@roles(M[11])
def pipeline_offline_process(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[11], cmd)


@roles(M[12])
def pipeline_parse_article(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[12], cmd)


@roles(M[13])
def pipeline_parse_list(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[13], cmd)


@roles(M[14])
def pipeline_publish_name(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[14], cmd)


@roles(M[15])
def pipeline_third_party(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[15], cmd)


@roles(M[16])
def pipeline_relate_news(cmd):
    assert cmd in COMMANDS
    _supervisor_pipeline(M[16], cmd)


@roles(M[17])
def spider_baidu(cmd):
    """通过 supervisorctl 命令管理该任务, cmd:start, stop, restart, status"""
    assert cmd in COMMANDS
    _supervisor_pipeline(M[17], cmd)


@roles(M[18])
def spider_haowai(cmd):
    """通过 supervisorctl 命令管理该任务, cmd:start, stop, restart, status"""
    assert cmd in COMMANDS
    _supervisor_pipeline(M[18], cmd)


@roles(M[19])
def thirdparty(cmd):
    """通过 supervisorctl 命令管理该任务, cmd:start, stop, restart, status"""
    assert cmd in COMMANDS
    _supervisor_pipeline(M[19], cmd)


DOCKER_CODE_SPACE = "/codespace"
DOCKER_PROJECTS = ["article-parser", "judge-page", "list-parser", "service-api"]
SERVICES = {
    "grpc-article-parser": "docker service create --name grpc-article-parser --network inner-network --replicas 3 --mount type=bind,src=/codespace/article-parser/article-parser,dst=/codespace leesven/python-grpc-spider-env",
    "grpc-list-parser": "docker service create --name grpc-list-parser --network inner-network --replicas 3 --mount type=bind,src=/codespace/list-parser/list-parser,dst=/codespace leesven/python-grpc-spider-env",
    "grpc-judge-page": "docker service create --name grpc-judge-page --network inner-network --replicas 3 --mount type=bind,src=/codespace/judge-page/judge-page,dst=/codespace leesven/python-grpc-spider-env",
    "http-service-api": "docker service create --name http-service-api --network inner-network --publish 8080:8080 --replicas 3 --mount type=bind,src=/codespace/service-api/bin,dst=/codespace ubuntu /codespace/service-api",
}


def _pull_parser_service(project):
    with cd(os.path.join(DOCKER_CODE_SPACE, project)):
        run("git pull")


@roles("swarm-server")
def rm_services(service=None):
    """删除解析服务,参数service=None,表示所有;可取值:grpc-article-parser,grpc-list-parser,grpc-judge-page,http-service-api"""
    if service is None:
        for service in SERVICES:
            run("docker service rm %s" % service)
    else:
        run("docker service rm %s" % service)


@roles("swarm-server")
def create_services(service=None):
    """新建解析服务,参数service=None,表示所有;可取值:grpc-article-parser,grpc-list-parser,grpc-judge-page,http-service-api"""
    if service is None:
        for service in SERVICES:
            run(SERVICES[service])
    else:
        run(SERVICES[service])


@roles("swarm-server")
def restart_services(service=None):
    """重启解析服务,参数service=None,表示所有;可取值:grpc-article-parser,grpc-list-parser,grpc-judge-page,http-service-api"""
    if service is None:
        for service in SERVICES:
            rm_services(service=service)
            time.sleep(4)
            create_services(service=service)
    else:
        rm_services(service=service)
        time.sleep(4)
        create_services(service=service)


@roles("swarm-server")
def ls_services():
    """列出正在运行的服务"""
    run("docker service ls")
