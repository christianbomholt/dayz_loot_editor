
import dao
import items
import windows
import xmlParser

def exportSpawnable():
    fname = windows.saveAsFile("xml", "w+")
    if fname is not None:
        spawnable = ""
        rifles = xmlParser.itemFromRows(dao.getType("rifles"))
        pistols = xmlParser.itemFromRows(dao.getType("pistols"))
        gun = xmlParser.itemFromRows(dao.getType("gun"))

        items = gun + rifles + pistols
        for item in items:
            if item.mod != "Vanilla":
                if item.nominal != 0:
                    spawnable += item.getSpawnableTypes()
        fname.write(spawnable)



    def getSpawnableTypes(self):
        linkedItems = dao.getLinekd(self.name, self.type)

        magChance = "0.30"
        opticChance = "0.10"
        attachmentChance = "0.20"

        mags = []
        optics = []
        buttstocks = []
        handguards = []
        otherAttachments = []

        for linkedItem in linkedItems:
            if linkedItem.type == "mag":
                mags.append(linkedItem)
            if linkedItem.type == "optic":
                optics.append(linkedItem)
            if linkedItem.type == "attachment":
                if linkedItem.subtype.lower() == "handguard":
                    handguards.append(linkedItem)
                elif linkedItem.subtype.lower() == "buttstock":
                    buttstocks.append(linkedItem)
                else:
                    otherAttachments.append(linkedItem)

        type = ""
        type += "  <type name=\"{}\">\n".format(self.name)
        type += attachmentBlock(mags, magChance)
        type += attachmentBlock(optics, opticChance)
        type += attachmentBlock(handguards, float(1.0))
        type += attachmentBlock(buttstocks, float(1.0))
        type += attachmentBlock(otherAttachments, attachmentChance)

        type += "  </type>\n"

        return type


def attachmentBlock(items, chance):
    type = ""
    if len(items) != 0:
        type += "    <attachments chance=\"{}\">\n".format(chance)
        for item in items:
            type += "      <item name=\"{}\" chance=\"{}\" />\n".format(item.name, round(1.0 / len(items), 2))

        type += "    </attachments>\n"

    return type        