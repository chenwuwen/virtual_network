# -*-coding:utf-8-*-
'''
开启热点配置：
    windows下开启热点,需要将目前连接网络的适配器(是本地网络入口的适配器，不是刚刚新建的)右键--->共享---->勾选允许其他网络用户链接，
'''
OS = {
    "WINDOWS": {
        "CREATE_HOST": "netsh wlan set hostednetwork mode=allow ssid=WIFI_NAME key=WIFI_PASSWORD",
        "START_HOT": "netsh wlan start hostednetwork",
        "STOP_HOT": "netsh wlan stop hostednetwork"
    },
    "LINUX": {
        "CREATE_HOST": "netsh wlan set hostednetwork mode=allow ssid=WIFI_NAME key=WIFI_PASSWORD",
        "START_HOT": "netsh wlan start hostednetwork"
    }
}
