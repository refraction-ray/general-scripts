import sys
from socket import gaierror
from urllib.error import URLError
from datetime import datetime
import json

user = sys.argv[2]  ## hardcoded into script filter in alfred workflow
passw = sys.argv[3]
if len(sys.argv) > 3:
    tunet_path = sys.argv[4]
    sys.path.append(tunet_path)
import tunet  ## see packages https://github.com/yuantailing/tunet-python

## bash script for alfred workflow as
## /path/python3 /path/netstatus.py $1 username password /path/for/tunet


def login(user, passw):
    network = "unknown"
    try:
        r = tunet.auth4.login(user, passw, net=True)
        if r["error"] == "ok" or r["error"] == "ip_already_online_error":
            network = "auth4 网络"
            tunet.net.login(
                user, passw
            )  # with already login auth and logout net, net cannot be login even with net=True
            return 0, network
        elif r["error_msg"].startswith("E2833"):
            network = "只支持 net 网络"
            ## network doesn't support auth
    except (gaierror, URLError):
        pass
    try:
        r = tunet.net.login(user, passw)
        if (
            r["msg"] == "IP has been online, please logout."
            or r["msg"] == "Login is successful."
        ):
            return 0, network
    except (gaierror, URLError):
        network = "非校园网络"
        return 1, network


def check():
    try:
        r = tunet.net.checklogin()
        if not r:
            return {"err": "not login"}
        r["err"] = "ok"
        return r
    except (gaierror, URLError):
        return {"err": "not with tsinghua network"}


def display():
    r = check()
    if r["err"] != "ok":
        res = {"items": [{"title": "未登录"}]}
    else:
        res = []
        res.append({"title": "用户", "subtitle": r["username"]})
        res.append(
            {
                "title": "登录时间",
                "subtitle": datetime.strftime(
                    datetime.fromtimestamp(r["time_login"]), "%Y-%m-%d, %H:%M"
                ),
            }
        )
        res.append({"title": "网费余额", "subtitle": "%.2f 元" % float(r["balance"])})
        res.append(
            {
                "title": "已用流量",
                "subtitle": "%.2f G" % (float(r["cumulative_incoming"]) / 1000.0 ** 3),
            }
        )
        res.append(
            {
                "title": "在用流量",
                "subtitle": "%.2f M" % (float(r["session_incoming"]) / 1000.0 ** 2),
            }
        )
        res = {"items": res}
    print(json.dumps(res))


def logout():
    try:
        tunet.net.logout()
    except tunet.NotLoginError:
        pass
    try:
        tunet.auth4.logout()
    except tunet.NotLoginError:
        pass


if __name__ == "__main__":
    if sys.argv[1] == "check" or sys.argv[1] == "ck":
        display()
    elif sys.argv[1] == "login" or sys.argv[1] == "in":
        st, nw = login(user, passw)
        b = {0: "成功", 1: "失败"}
        print(json.dumps({"items": [{"title": "登录" + nw + b[st]}]}))
    elif sys.argv[1] == "logout" or sys.argv[1] == "out":
        logout()
        print(json.dumps({"items": [{"title": "退出登录"}]}))
