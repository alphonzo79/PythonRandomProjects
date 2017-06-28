from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LEDGER, portrait
import sys

onePoint = 1.0 / 72
oneInch = 72.0
leftEdge = 0.0
rightEdge = 11.0 * oneInch
bottomEdge = 0.0
topEdge = 17.0 * oneInch
margin = 0.5 * oneInch

if len(sys.argv) < 3:
	print "You need to provide a file name and at least one line resolution"
	exit()

c = canvas.Canvas(sys.argv[1] + ".pdf", portrait(LEDGER))
c.setStrokeColorRGB(0,0,0)

left = leftEdge + margin
bottom = bottomEdge + margin
height = oneInch * 3
argIndex = 2

while bottom < topEdge - margin:
	if bottom + height > topEdge - margin:
		height = topEdge - margin - bottom

	resolution = 133
	if argIndex < len(sys.argv):
		resolution = int(sys.argv[argIndex])
	
	lineWidthInches = 1.0 / (resolution * 2)
	lineWidthPoints = lineWidthInches / onePoint
	c.setLineWidth(lineWidthPoints)

	while left < rightEdge - margin:
		c.line(left, bottom, left, bottom + height)
		left = left + (lineWidthPoints * 2)

	c.setFillColorRGB(0,0,0)
	c.rect(leftEdge + margin, bottom + height - 20, 40, 20, 0, 1)
	c.setFillColorRGB(256,256,256)
	c.drawCentredString(leftEdge + margin + 20, bottom + height - 14, str(resolution))

	argIndex += 1
	left = leftEdge + margin
	bottom = bottom + height + (margin * 0.7)

c.save()