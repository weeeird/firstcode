from lxml import etree
import asyncio
import aiohttp
import aiofiles


async def getpagecontent(url, href, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url + href, headers=headers) as r:
            html = etree.HTML(await r.text())
            name = html.xpath("/html/body/div[2]/section[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/p/span/text()")[0]
            time = html.xpath("/html/body/div[2]/section[1]/div/div[2]/div[1]/div[2]/div[2]"
                              "/div[1]/div/div[2]/a/span[1]/text()")[0]
            score = html.xpath("/html/body/div[2]/section[1]/div/div[2]/div[2]/a/div[2]/div[2]/div/span[1]/text()")[0]
            # total = html.xpath("/html/body/div[2]/section[1]/div/div[2]/a/div/div[3]/div[1]/p[2]/span[1]/text()")[0]
            csv_line = format_csv_line(name, time, score)

            async with aiofiles.open("data_detail.csv", mode="a", encoding="utf-8") as f:
                await f.write(csv_line + "\n")  # 添加换行符


async def gethref(url):
    url_ = url + "/rankings/year"

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0,',
            'Cookie': '_lxsdk_cuid=18e4a14dd54c8-04bc5d29d7f4f8-4c657b58-144000-18e4a14dd54c8; _lxsdk=03162560E40011EE819FC935B2C3306B2B5C2D61FECB4EB7AA4548DCC107F389; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1710639921; theme=moviepro; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _lxsdk_s=18f561ed30c-ac8-af-3cf%7C%7C14',
        }

    async with aiohttp.ClientSession() as session:
        async with session.get(url_, headers=headers) as resp:
            main_page = etree.HTML(await resp.text())

            uls = main_page.xpath('//div[@id="ranks-list"]/ul')

            task = []

            for ul in uls:
                # 注意：这里可能需要修改 XPath 或其他方法来正确提取 href
                href = ul.xpath('./@data-com')[0].split("'")[-2]  # 假设 href 在 <a> 标签的 href 属性中
                task.append(asyncio.create_task(getpagecontent(url, href, headers)))
            await asyncio.wait(task)


def format_csv_line(name, time, score):
    # 这里是一个简单的示例，你可能需要根据实际需求调整格式
    return f"{name},{time},{score}"


async def main():
    url = "https://piaofang.maoyan.com"  # 替换为你的基础 URL
    await gethref(url)


if __name__ == '__main__':
    asyncio.run(main())



