import requests
from yt_dlp import YoutubeDL

api_key = "AIzaSyBlcLcNPbiF8e1cFuSSypJ1krhbCBNd1aM"

global params
global cookies
global headers

cookies = {
    'VISITOR_INFO1_LIVE': 'ZHSiuzWZi44',
    'HSID': 'A0b-VDVTvMJQHetMc',
    'SSID': 'A1PmV7OVYgkN8hdNK',
    'APISID': 'r8VDVlJ8dgVZqNHM/AqKndNTJfO6lvgvgD',
    'SAPISID': 'LtXIXcJd5_9etNs7/AjO_24zKmaqexC1Ha',
    '__Secure-1PAPISID': 'LtXIXcJd5_9etNs7/AjO_24zKmaqexC1Ha',
    '__Secure-3PAPISID': 'LtXIXcJd5_9etNs7/AjO_24zKmaqexC1Ha',
    'LOGIN_INFO': 'AFmmF2swRAIgFfdLI0coCdR8wAKnPxOPaCFxF1q8xBdDt1yP1KSkYnUCIAmtiGrJWMm9Eot9a7v-z5l4g7RniHAVRuunxFCCU11l:QUQ3MjNmeEZBMG8yQWxpMURuUDNjUml4Nk15UXBmTEpnWUc3QjZPWFZkdlZzRFhGRzJmSXNjZHpFcHA2ZHl1TkJoTjB0RWFQZkRHOGRDV1I4VkhsT01YSnZfcFZFb0FUanlPQmJnTjlMcTZHdFNaQWdRdXc4V2J4b0lBTlBPQkpBZEJ4STJHalQ4UEdqbHY0bFhjSVcyNlpyODB6UlZBQU1B',
    'SID': 'OwiYgYV-DcUwZwMI-ExMgphOtOkRtFTdG7cjALAKv7Uucg1GrQhNqsK8xCUpGw8zKMqdCQ.',
    '__Secure-1PSID': 'OwiYgYV-DcUwZwMI-ExMgphOtOkRtFTdG7cjALAKv7Uucg1GFWoHYYn9ZZvSa__FW4RTXg.',
    '__Secure-3PSID': 'OwiYgYV-DcUwZwMI-ExMgphOtOkRtFTdG7cjALAKv7Uucg1GK8cRG09lFtmw2mjBfo66ZA.',
    'PREF': 'tz=Asia.Yekaterinburg&f4=4000000',
    'YSC': 'LLId-sr0oVs',
    'SIDCC': 'AEf-XMSlLH72t4xr1P7jYnGcVoMMQBFCbDCVV4Xp07oZSfpIR39aSMyktCZqupLKr12ClARcxw',
    '__Secure-1PSIDCC': 'AEf-XMTkjLJ2Yh4d2nYRFHnHzrCU6HEy0NFrzwC6cfmFKxxkhfRZSj0DmFCJXYbKVj64m8zQx1o',
    '__Secure-3PSIDCC': 'AEf-XMRz5sUy6z2mtZ6Ct2ll7CXt93H_OnWHn6mhlMxLaeTLLegZSCmPfnCeR4z-o6YR-iyT1Zs',
    'ST-37hutb': 'oq=pc_connect%20%D0%BD%D0%B5%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D1%82%D1%81%D1%8F&gs_l=youtube.12...0.0.1.115484.0.0.0.0.0.0.0.0..0.0.uqap13nmrh2%2Cytpo-bo-me%3D1%2Cytposo-bo-me%3D1%2Cytpo-bo-ro-erqs%3D0%2Cytpo-bo-ro-erq%3D0%2Cytposo-bo-ro-erqs%3D0%2Cytposo-bo-ro-erq%3D0%2Cytpo-bo-ro-mi%3D24260295%2Cytposo-bo-ro-mi%3D24260295%2Ccfro%3D1%2Cytpo-bo-me%3D0%2Cytposo-bo-me%3D0...0...1ac..64.youtube..0.0.0....0.lJJAbBlPJs0&itct=CBYQ7VAiEwju8Y2_h9H6AhVVx08IHe_hBzM%3D&csn=MC42NDQ2MzMyNTExMDg4MDMx&endpoint=%7B%22clickTrackingParams%22%3A%22CBYQ7VAiEwju8Y2_h9H6AhVVx08IHe_hBzM%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fresults%3Fsearch_query%3Dpc_connect%2B%25D0%25BD%25D0%25B5%2B%25D1%2583%25D1%2581%25D1%2582%25D0%25B0%25D0%25BD%25D0%25B0%25D0%25B2%25D0%25BB%25D0%25B8%25D0%25B2%25D0%25B0%25D0%25B5%25D1%2582%25D1%2581%25D1%258F%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_SEARCH%22%2C%22rootVe%22%3A4724%7D%7D%2C%22searchEndpoint%22%3A%7B%22query%22%3A%22pc_connect%20%D0%BD%D0%B5%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D1%82%D1%81%D1%8F%22%7D%7D',
}

headers = {
    'authority': 'www.youtube.com',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'authorization': 'SAPISIDHASH 1665246846_536e8f3a4c1642098ca03771dc742dd44f8d2ba5',
    'cookie': 'VISITOR_INFO1_LIVE=ZHSiuzWZi44; HSID=A0b-VDVTvMJQHetMc; SSID=A1PmV7OVYgkN8hdNK; APISID=r8VDVlJ8dgVZqNHM/AqKndNTJfO6lvgvgD; SAPISID=LtXIXcJd5_9etNs7/AjO_24zKmaqexC1Ha; __Secure-1PAPISID=LtXIXcJd5_9etNs7/AjO_24zKmaqexC1Ha; __Secure-3PAPISID=LtXIXcJd5_9etNs7/AjO_24zKmaqexC1Ha; LOGIN_INFO=AFmmF2swRAIgFfdLI0coCdR8wAKnPxOPaCFxF1q8xBdDt1yP1KSkYnUCIAmtiGrJWMm9Eot9a7v-z5l4g7RniHAVRuunxFCCU11l:QUQ3MjNmeEZBMG8yQWxpMURuUDNjUml4Nk15UXBmTEpnWUc3QjZPWFZkdlZzRFhGRzJmSXNjZHpFcHA2ZHl1TkJoTjB0RWFQZkRHOGRDV1I4VkhsT01YSnZfcFZFb0FUanlPQmJnTjlMcTZHdFNaQWdRdXc4V2J4b0lBTlBPQkpBZEJ4STJHalQ4UEdqbHY0bFhjSVcyNlpyODB6UlZBQU1B; SID=OwiYgYV-DcUwZwMI-ExMgphOtOkRtFTdG7cjALAKv7Uucg1GrQhNqsK8xCUpGw8zKMqdCQ.; __Secure-1PSID=OwiYgYV-DcUwZwMI-ExMgphOtOkRtFTdG7cjALAKv7Uucg1GFWoHYYn9ZZvSa__FW4RTXg.; __Secure-3PSID=OwiYgYV-DcUwZwMI-ExMgphOtOkRtFTdG7cjALAKv7Uucg1GK8cRG09lFtmw2mjBfo66ZA.; PREF=tz=Asia.Yekaterinburg&f4=4000000; YSC=LLId-sr0oVs; SIDCC=AEf-XMSlLH72t4xr1P7jYnGcVoMMQBFCbDCVV4Xp07oZSfpIR39aSMyktCZqupLKr12ClARcxw; __Secure-1PSIDCC=AEf-XMTkjLJ2Yh4d2nYRFHnHzrCU6HEy0NFrzwC6cfmFKxxkhfRZSj0DmFCJXYbKVj64m8zQx1o; __Secure-3PSIDCC=AEf-XMRz5sUy6z2mtZ6Ct2ll7CXt93H_OnWHn6mhlMxLaeTLLegZSCmPfnCeR4z-o6YR-iyT1Zs; ST-37hutb=oq=pc_connect%20%D0%BD%D0%B5%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D1%82%D1%81%D1%8F&gs_l=youtube.12...0.0.1.115484.0.0.0.0.0.0.0.0..0.0.uqap13nmrh2%2Cytpo-bo-me%3D1%2Cytposo-bo-me%3D1%2Cytpo-bo-ro-erqs%3D0%2Cytpo-bo-ro-erq%3D0%2Cytposo-bo-ro-erqs%3D0%2Cytposo-bo-ro-erq%3D0%2Cytpo-bo-ro-mi%3D24260295%2Cytposo-bo-ro-mi%3D24260295%2Ccfro%3D1%2Cytpo-bo-me%3D0%2Cytposo-bo-me%3D0...0...1ac..64.youtube..0.0.0....0.lJJAbBlPJs0&itct=CBYQ7VAiEwju8Y2_h9H6AhVVx08IHe_hBzM%3D&csn=MC42NDQ2MzMyNTExMDg4MDMx&endpoint=%7B%22clickTrackingParams%22%3A%22CBYQ7VAiEwju8Y2_h9H6AhVVx08IHe_hBzM%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fresults%3Fsearch_query%3Dpc_connect%2B%25D0%25BD%25D0%25B5%2B%25D1%2583%25D1%2581%25D1%2582%25D0%25B0%25D0%25BD%25D0%25B0%25D0%25B2%25D0%25BB%25D0%25B8%25D0%25B2%25D0%25B0%25D0%25B5%25D1%2582%25D1%2581%25D1%258F%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_SEARCH%22%2C%22rootVe%22%3A4724%7D%7D%2C%22searchEndpoint%22%3A%7B%22query%22%3A%22pc_connect%20%D0%BD%D0%B5%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D1%82%D1%81%D1%8F%22%7D%7D',
    'origin': 'https://www.youtube.com',
    'referer': 'https://www.youtube.com/results?search_query=pc_connect+%D0%BD%D0%B5+%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D1%82%D1%81%D1%8F',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Yandex";v="22"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"22.9.2.1495"',
    'sec-ch-ua-full-version-list': '"Chromium";v="104.0.5112.124", " Not A;Brand";v="99.0.0.0", "Yandex";v="22.9.2.1495"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'same-origin',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 Safari/537.36',
    'x-goog-authuser': '0',
    'x-goog-visitor-id': 'CgtaSFNpdXpXWmk0NCiTy4aaBg%3D%3D',
    'x-origin': 'https://www.youtube.com',
    'x-youtube-bootstrap-logged-in': 'true',
    'x-youtube-client-name': '1',
    'x-youtube-client-version': '2.20221006.09.00',
}

params = {
    'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
    'prettyPrint': 'false',
}

def music(url, check=True):
    if check == False:
        track = url
    elif "http" in url:
        try: listId = url.split('list=')[1].split('&')
        except: listId = None

        if listId:
            track = playlistIds(listId[0])
        else:
            track = url
    else:
        track = search(url)

    with YoutubeDL() as ydl:
        ydl_info = ydl.extract_info(track, download=False)
        rtn = {
            'title': ydl_info['title'],
            'img': ydl_info['thumbnails'][26]['url']
        }
        return [ydl_info['formats'][5]['url'], rtn]

def playlistIds(playlistId):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=500&playlistId={playlistId}&key={api_key}"

    urls = []

    r = requests.get(url)

    for id in r.json()['items']:
        urls.append('https://www.youtube.com/watch?v=' + id['snippet']['resourceId']['videoId'])
    
    return urls


def search(query):
    global params
    global cookies
    global headers

    json_data = {
        'context': {
            'client': {
                'hl': 'ru',
                'gl': 'RU',
                'remoteHost': '178.176.113.200',
                'deviceMake': '',
                'deviceModel': '',
                'visitorData': 'CgtaSFNpdXpXWmk0NCiTy4aaBg%3D%3D',
                'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 Safari/537.36,gzip(gfe)',
                'clientName': 'WEB',
                'clientVersion': '2.20221006.09.00',
                'osName': 'Windows',
                'osVersion': '10.0',
                'originalUrl': 'https://www.youtube.com/results?search_query=pc_connect+%D0%BD%D0%B5+%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D1%82%D1%81%D1%8F',
                'screenPixelDensity': '1',
                'platform': 'DESKTOP',
                'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
                'configInfo': {
                    'appInstallData': 'CJPLhpoGELiLrgUQ4rmuBRDB0K4FEJOJ_hIQy-z9EhC3y60FEJnGrgUQ28quBRDUg64FEJTPrgUQ6squBRDri_4SEJjIrgUQqrKuBRDYvq0FEJH4_BI%3D',
                },
                'screenDensityFloat': '1.100000023841858',
                'timeZone': 'Asia/Yekaterinburg',
                'browserName': 'Chrome',
                'browserVersion': '104.0.5112.124',
                'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'screenWidthPoints': '812',
                'screenHeightPoints': '725',
                'utcOffsetMinutes': '300',
                'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT',
                'memoryTotalKbytes': '8000000',
                'mainAppWebInfo': {
                    'graftUrl': '/results?search_query=pc_connect+%D0%BD%D0%B5+%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%B0%D0%B2%D0%BB%D0%B8%D0%B2%D0%B0%D0%B5%D1%82%D1%81%D1%8F',
                    'pwaInstallabilityStatus': 'PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED',
                    'webDisplayMode': 'WEB_DISPLAY_MODE_BROWSER',
                    'isWebNativeShareAvailable': 'True',
                },
            },
            'user': {
                'lockedSafetyMode': 'False',
            },
            'request': {
                'useSsl': 'True',
                'internalExperimentFlags': [],
                'consistencyTokenJars': [],
            },
        },
        'query': query,
        'webSearchboxStatsUrl': f'/search?oq={query}&gs_l=youtube.12...0.0.1.115484.0.0.0.0.0.0.0.0..0.0.uqap13nmrh2,ytpo-bo-me=1,ytposo-bo-me=1,ytpo-bo-ro-erqs=0,ytpo-bo-ro-erq=0,ytposo-bo-ro-erqs=0,ytposo-bo-ro-erq=0,ytpo-bo-ro-mi=24260295,ytposo-bo-ro-mi=24260295,cfro=1,ytpo-bo-me=0,ytposo-bo-me=0...0...1ac..64.youtube..0.0.0....0.lJJAbBlPJs0',
    }

    try:
        r = requests.post('https://www.youtube.com/youtubei/v1/search', params=params, cookies=cookies, headers=headers, json=json_data)
        for x in r.json()['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
            try: 
                Video = x ['videoRenderer']['navigationEndpoint']['watchEndpoint']

                if 'playlistId' in Video:
                    listId = Video['playlistId']
                elif 'videoId' in Video:
                    Id = Video['videoId']
                
                url = f"https://www.youtube.com/watch?v={Id}"
                break
            
            except:
                pass

    except:
        url = "https://www.googleapis.com/youtube/v3/search"

        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'key': api_key
        }

        r = requests.get(url, params=params)

        try: Video = r.json()['items'][0]['id']
        except: print(r.json())
        
        if 'playlistId' in Video:
            url = playlistIds(Video['playlistId'])

        elif 'videoId' in Video:
            url = f"https://www.youtube.com/watch?v={Video['videoId']}"

    return url
