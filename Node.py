class Node():
	def __init__(self,title,color=None,debug=False) -> None:
		# self.logger = Logger(f"Node({title})",debug=debug)
		self.data = {
			"title":title,
			"data":[],
			"image":None,
		}
		self._children = []

	def addDataField(self,datatype,data):
		self.data["data"].append({datatype:data})

	def removeDataField(self,datatype,data):
		self.data["data"].remove({datatype:data})

	def addImage(self,imagetype,imageUrl):
		self.data["image"] = {imagetype:imageUrl}