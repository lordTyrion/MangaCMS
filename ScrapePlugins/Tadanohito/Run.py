

from ScrapePlugins.Tadanohito.DbLoader import DbLoader
from ScrapePlugins.Tadanohito.ContentLoader import ContentLoader

import runStatus

import ScrapePlugins.RunBase

class Runner(ScrapePlugins.RunBase.ScraperBase):


	loggerPath = "Main.Manga.Tadanohito.Run"
	pluginName = "Tadanohito"



	def _go(self):
		fl = DbLoader()
		fl.go()
		fl.closeDB()


		if not runStatus.run:
			return

		cl = ContentLoader()
		cl.go()
		cl.closeDB()


if __name__ == "__main__":
	import utilities.testBase as tb

	with tb.testSetup(startObservers=False):
		run = Runner()
		run.go()
