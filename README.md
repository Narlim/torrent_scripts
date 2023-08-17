# torrent_scripts
download free torrents

## opencd
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
5/* * * * * python /torrent/opencd_free_torrents.py >> /var/log/opencd_download_torrents.log
```

## MT
### set cookies and kind
```
kind = "movie.php" # for example

cookies = {
    "tp": "" # get it from console http request.
}          
```

### set crontab
```
5/* * * * * python /torrent/mt_free_torrents.py >> /var/log/mt_download_torrents.log
```

## set qbittorrent
设置监控文件夹，会自动下载新增的种子
