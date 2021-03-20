import configparser
import datetime
import logging
import os
import re

from jenkinsapi.jenkins import Jenkins

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]-[%(name)s]-[%(levelname)s]-%(message)s')
log = logging.getLogger(__name__)


def get_jk_config(chose):
    """
    读取配置文件获得各项参数,再拼接成url
    :param chose: 配置文件中的label名
    :return: url, username, password
    """
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'jenkins_server.ini'))
    username = config.get(chose, 'username')
    password = config.get(chose, 'password')
    host = config.get(chose, 'host')
    port = config.get(chose, 'port')
    url = 'http://' + host + ':' + port
    return url, username, password


# def test_run_jenkins_job():
#     jk = JenkinsAPIDemo("demo_a")
#     jk.run()


class JenkinsAPIDemo:
    def __init__(self, job_name, chose='jenkins'):
        self.job_name = job_name
        config = get_jk_config(chose)
        self.jk = Jenkins(*config, useCrumb=True)  # 解元组,作为Jenkins的参数
        print(self.jk)

    def __get_job_from_keys(self):
        """
        对job_name做模糊匹配,一旦匹配到则将jk.keys中的一个添加到列表
        :return:
        """
        choose_list = []
        print(self.jk.keys())
        for my_job_name in self.jk.keys():
            if self.job_name in my_job_name:
                choose_list.append(my_job_name)
        return choose_list

    def __job_build(self, my_job_name):
        if self.jk.has_job(my_job_name):
            # 如果job存在,则获取这个job
            my_job = self.jk.get_job(my_job_name)
            # 如果job不在跑或者等待就开始一次运行
            if not my_job.is_queued_or_running():
                try:
                    last_build = my_job.get_last_buildnumber()
                except:
                    last_build = 0
                build_num = last_build + 1
                print(f"即将开始的构建id: {build_num}")
                # 开始跑一次任务
                try:
                    self.jk.build_job(my_job_name)
                except Exception as e:
                    log.error(str(e))
                # 循环判断任务是否run完成
                while True:
                    # 如果任务停止运行了
                    if not my_job.is_queued_or_running():
                        # 获取最新一次打包信息
                        count_build = my_job.get_build(build_num)
                        # 获取运行开始时间
                        start_time = count_build.get_timestamp() + datetime.timedelta(
                            hours=8)  # 如果jenlins每调时区,加上8个小时就显示中国时间
                        # 获取运行日志
                        console_out = count_build.get_console()
                        # print(console_out)
                        # 获取状态
                        status = count_build.get_status()
                        # 获取变更内容
                        change = count_build.get_changeset_items()
                        print("变化为:")
                        print(change)
                        log.info(" " + str(start_time) + " 发起的" + my_job_name + "构建已经完成")
                        # 根据正则匹配
                        p2 = re.compile(r".*ERROR.*")
                        err_list = p2.findall(console_out)
                        print("错误日志:")
                        print(err_list)
                        log.info(" 打包日志为:" + str(console_out))
                        if status == "SUCCESS":
                            if len(change) > 0:
                                for data in change:
                                    for file_list in data["affectedPaths"]:
                                        log.info(" 发起的 " + my_job_name + " 变更的类: " + file_list)
                                    log.info(" 发起的 " + my_job_name + " 变更的备注: " + data["msg"])
                                    log.info(" 发起的 " + my_job_name + " 变更的提交人: " + data["author"]["fullName"])
                            else:
                                log.info(" 发起的 " + my_job_name + " 构建没有变更内容! ")
                            if len(err_list) > 0:
                                log.warning(" 构建的 " + my_job_name + "构建状态成功,但包含了以下错误:")
                                for error in err_list:
                                    log.error(error)
                        else:
                            if len(err_list) > 0:
                                log.warning(" 构建的 " + my_job_name + "包含了以下错误:")
                                for error in err_list:
                                    log.error(error)
                        break
            else:
                log.warning(" 发起的 " + my_job_name + " Jenkins is running")
        else:
            log.warning(" 发起的 " + my_job_name + " 没有该服务")

    def run(self):
        my_job_name = self.__get_job_from_keys()
        if len(my_job_name) == 1:
            self.__job_build(my_job_name[0])
        elif len(my_job_name) == 0:
            log.error(" 输入的job名不正确! ")


if __name__ == '__main__':
    jk = JenkinsAPIDemo("demo_a")
    jk.run()
