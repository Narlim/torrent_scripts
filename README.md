# torrent_scripts
download free torrents

### set opencd cookies
```
cookies = {
    "_ga": "",
    "_ga_J6J9PS1H9S": "",
    "c_lang_folder": "cht",
    "c_secure_login": "",
    "c_secure_pass": "",
    "c_secure_ssl": "",
    "c_secure_tracker_ssl": "",
    "c_secure_uid": ""
}
```

### set crontab
```
5/* * * * * python /torrent/opencd_free_torrents.py >> /var/log/download_torrents.log
```

### set qbittorrent
设置监控文件夹，会自动下载新增的种子