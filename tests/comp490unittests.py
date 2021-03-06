import unittest
import aiohttp
import click
import ssl
from click.testing import CliRunner
import twtxt.models
import twtxt.twhttp
import twtxt.config
import twtxt.cli
import twtxt.cache
import asyncio
#490compsci
class MyTestCase(unittest.TestCase):
    def test_301url_reroute(self):
        config=twtxt.config.Config.discover()
        name="patrick"
        url="http://127.0.0.1:8081/"
        source=twtxt.models.Source(name,url)
        config.add_source(source)
        cache=twtxt.cache.Cache.discover()
        with aiohttp.ClientSession() as client:
            loop = asyncio.get_event_loop()
            s=loop.run_until_complete(twtxt.twhttp.retrieve_file(client,source,30,cache))

        config=twtxt.config.Config.discover()
        newSOurce=config.get_source_by_nick(name)

        self.assertNotEqual(newSOurce.url,url)
    def test_301reroute_doesnot_effectgoodsources(self):
        config=twtxt.config.Config.discover()
        name="mdom"
        url="https://mdom.github.io/twtxt.txt"
        source=twtxt.models.Source(name,url)
        config.add_source(source)
        with aiohttp.ClientSession() as client:
            twtxt.twhttp.retrieve_file(client,source,30,config)
        newSOurce=config.get_source_by_nick(name)
        self.assertEqual(newSOurce.url,url)
    def test_aiohttpdoesnotCrashProgramWhenSOurceCannotBeRead(self):

        runner = CliRunner()
        self.assertNotEqual(runner.invoke(twtxt.cli.cli,['view','http://codemachine1.github.io/twtxt.txt']),None)

    def test_iferroristhrownWhenConnectingToPageWithCertificateWithWrongname(self):
        config=twtxt.config.Config.discover()
        name="mdom"
        url="https://wrong.host.badssl.com/"
        source=twtxt.models.Source(name,url)
        cache=twtxt.cache.Cache.discover()
        config.add_source(source)
        with aiohttp.ClientSession() as client:
            loop = asyncio.get_event_loop()
            testoutput=loop.run_until_complete(twtxt.twhttp.retrieve_file(client,source,30,cache))
            self.assertEquals(testoutput,[])
    def test_iferroristhrownWhenConnectingTyoPageWithExpiredCertificate(self):
        config=twtxt.config.Config.discover()
        name="mdom"
        url="https://expired.badssl.com/"
        source=twtxt.models.Source(name,url)
        cache=twtxt.cache.Cache.discover()
        config.add_source(source)
        with aiohttp.ClientSession() as client:
            loop = asyncio.get_event_loop()
            testoutput=loop.run_until_complete(twtxt.twhttp.retrieve_file(client,source,30,cache))
            self.assertEquals(testoutput,[])






if __name__ == '__main__':
    unittest.main()
