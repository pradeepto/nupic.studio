from nustudio.htm import maxStoredSteps
from nustudio.ui import Global

class Cell:
	"""
	A class only to group properties related to cells.
	"""

	#region Constructor

	def __init__(self):
		"""
		Initializes a new instance of this class.
		"""

		#region Instance fields

		self.index = -1
		"""Index of this cell in the temporal pooler."""

		self.z = -1
		"""Position on Z axis"""

		self.segments = []
		"""List of distal segments of this cell."""

		# States of this element
		self.isLearning = [False] * maxStoredSteps
		self.isActive = [False] * maxStoredSteps
		self.isPredicted = [False] * maxStoredSteps

		#region Statistics properties

		self.statsActivationCount = 0
		self.statsActivationRate = 0.
		self.statsPreditionCount = 0
		self.statsPrecisionRate = 0.

		#endregion

		#region 3d-tree properties (simulation form)

		self.tree3d_initialized = False
		self.tree3d_x = 0
		self.tree3d_y = 0
		self.tree3d_z = 0
		self.tree3d_item = None
		self.tree3d_selected = False

		#endregion

		#endregion

	#endregion

	#region Methods

	def nextStep(self):
		"""
		Perfoms actions related to time step progression.
		"""

		# Update states machine by remove the first element and add a new element in the end
		if len(self.isActive) > maxStoredSteps:
			self.isLearning.remove(self.isLearning[0])
			self.isActive.remove(self.isActive[0])
			self.isPredicted.remove(self.isPredicted[0])

			# Remove segments (and their synapses) that are marked to be removed
			for segment in self.segments:
				if segment.isRemoved[0]:
					for synapse in segment.synapses:
						segment.synapses.remove(synapse)
						del synapse
					self.segments.remove(segment)
					del segment
		self.isLearning.append(False)
		self.isActive.append(False)
		self.isPredicted.append(False)

		for segment in self.segments:
			segment.nextStep()

		# Calculate statistics
		if self.isActive[maxStoredSteps - 1]:
			self.statsActivationCount += 1
		if self.isPredicted[maxStoredSteps - 1]:
			self.statsPreditionCount += 1
		if Global.currStep > 0:
			self.statsActivationRate = self.statsActivationCount / Global.currStep
		if self.statsActivationCount > 0:
			self.statsPrecisionRate = self.statsPreditionCount / self.statsActivationCount

	#endregion
