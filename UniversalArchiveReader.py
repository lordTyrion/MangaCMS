#!/usr/bin/python
# -*- coding: utf-8 -*-

import magic
import zlib

import zipfile
import rarfile

import logging
import traceback


class ArchiveReader(object):

	def __init__(self, archPath):
		self.logger = logging.getLogger("Main.ArchTool")
		self.archPath = archPath

		self.fType = magic.from_file(archPath, mime=True).decode("ascii")

		#print "wholepath - ", wholePath
		if self.fType == 'application/x-rar':
			#print "Rar File"
			self.archHandle = rarfile.RarFile(self.archPath) # self.iterRarFiles()
			self.archType = "rar"
		elif self.fType == 'application/zip':
			#print "Zip File"
			self.archHandle = zipfile.ZipFile(self.archPath) # self.iterZipFiles()
			self.archType = "zip"
		else:
			print("Returned MIME Type for file = ", self.fType )
			raise ValueError("Tried to create ArchiveReader on a non-archive file")

	def getFileList(self):
		names = self.archHandle.namelist()
		ret = []
		for name in names:

			try:
				if not self.archHandle.getinfo(name).isdir():
					ret.append(name)
			except:
				if not name.endswith("/"):
					ret.append(name)
		return ret


	def __iter__(self):
		try:
			if self.archType == "rar":
				for item in self.iterRarFiles():
					yield item
			elif self.archType == "zip":
				for item in self.iterZipFiles():
					yield item
			else:
				raise ValueError("Not a known archive type. Wat")

		except TypeError:
			self.logger.error("Empty Archive Directory? Path = %s", self.archPath)
			raise

		except (rarfile.BadRarFile, zipfile.BadZipfile):
			self.logger.error("CORRUPT ARCHIVE: ")
			self.logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				self.logger.error("%s", tbLine)
			raise

		except (rarfile.PasswordRequired, RuntimeError):
			self.logger.error("Archive password protected: ")
			self.logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				self.logger.error("%s", tbLine)
			raise


		except zlib.error:
			self.logger.error("Archive password protected: ")
			self.logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				self.logger.error("%s", tbLine)
			raise

		except (KeyboardInterrupt, SystemExit, GeneratorExit):
			raise

		except:
			self.logger.error("Unknown error in archive iterator: ")
			self.logger.error("%s", self.archPath)
			for tbLine in traceback.format_exc().rstrip().lstrip().split("\n"):
				self.logger.error("%s", tbLine)
			raise

	def getFileContentHandle(self, fileName):
		return self.archHandle.open(fileName)


	def iterZipFiles(self):
		names = self.getFileList()
		for name in names:
			with self.archHandle.open(name) as tempFp:
				yield name, tempFp



	def iterRarFiles(self):
		names = self.getFileList()
		for name in names:
			with self.archHandle.open(name) as tempFp:
				name = name.replace("\\", "/")
				yield name, tempFp

				#raise


	def close(self):
		self.archHandle.close()
