from enum import Enum, unique
import os


# %% Core (backend) functionality

@unique
class SetupMode(Enum):
    NEW = 0
    OLD = 1
    SYNTHETIC = 2  # used for creating a "fake" map.json

@unique
class Config(Enum):
    # system
    MESH = 'mesh'
    MATERIALS = 'materials'
    FIBER_Z = 'fiber_z'
    CUFFS = 'cuffs'
    EXCEPTIONS = 'exceptions'
    ENV = 'env'
    CI_PERINEURIUM_THICKNESS = 'ci_perineurium_thickness'
    PERINEURIUM_RESISTIVITY = 'perineurium_resistivity'

    # user
    RUN = 'run'
    SAMPLE = 'sample'
    MOCK_SAMPLE = 'mock_sample'
    MODEL = 'models'
    SIM = 'sims'
    CRITERIA = 'criteria'

@unique
class Object(Enum):
    SAMPLE = 'sample'
    SIMULATION = 'sim'

@unique
class Env(Enum):
    prefix = 'ASCENT_'

    COMSOL_PATH = prefix + 'COMSOL_PATH'
    JDK_PATH = prefix + 'JDK_PATH'
    PROJECT_PATH = prefix + 'PROJECT_PATH'
    NSIM_EXPORT_PATH = prefix + 'NSIM_EXPORT_PATH'

    vals = [
        COMSOL_PATH,
        JDK_PATH,
        PROJECT_PATH,
        NSIM_EXPORT_PATH
    ]
# %% Trace functionality

@unique
class DownSampleMode(Enum):
    KEEP = 0
    REMOVE = 1


class WriteMode(Enum):
    SECTIONWISE = 0
    SECTIONWISE2D = 1
    DATA = 2
    HOC = 3
    file_endings = ['.txt', '.txt', '.dat', '.hoc']


# %% Higher-level Manager functionality

@unique
class ReshapeNerveMode(Enum):
    config = 'reshape_nerve'

    CIRCLE = 0
    ELLIPSE = 1
    NONE = 3


@unique
class MaskInputMode(Enum):
    config = 'mask_input'

    INNERS = 0
    OUTERS = 1
    INNER_AND_OUTER_SEPARATE = 2
    INNER_AND_OUTER_COMPILED = 3


@unique
class MaskFileNames(Enum):
    RAW = 'r.tif'
    COMPILED = 'c.tif'
    INNERS = 'i.tif'
    OUTERS = 'o.tif'
    SCALE_BAR = 's.tif'
    NERVE = 'n.tif'
    ORIENTATION = 'a.tif'  # a for angle


@unique
class NerveMode(Enum):
    config = 'nerve'

    PRESENT = 1
    NOT_PRESENT = 0


@unique
class PopulateMode(Enum):
    config = 'populate_method'
    parameters = 'populate'

    EXPLICIT = 0
    TRUNCNORM = 1
    UNIFORM = 2


@unique
class DeformationMode(Enum):
    config = 'deform'

    NONE = None
    JITTER = 0
    PHYSICS = 1


# %% Fiber Position and Type

@unique
class FiberXYMode(Enum):
    config = 'fiber_xy'
    parameters = 'xy_parameters'

    UNIFORM_DENSITY = 0  # all fascicles have same fiber DENSITY, randomized positions within each fascicle
    UNIFORM_COUNT = 1  # all fascicles have save fiber COUNT, same randomization of positions within each fascicle
    CENTROID = 2  # a single fiber per inner trace (endoneurium bundle?), located at each inner trace centroid
    WHEEL = 3  # 1) points on lines extending radially for each inner centroid, 2) offset inwards from boundary
    SL_PSEUDO_INTERP = 4  # special mode for interpolating along approximate superior laryngeal branch of vagus nerve
    EXPLICIT = 5  # looks for explicit.txt in samples/#/models/#/sims/#/ directory for coordinates


@unique
class FiberZMode(Enum):
    config = 'fiber_z'
    parameters = 'z_parameters'

    EXTRUSION = 0
    LOFTED = 1


@unique
class ZOffsetMode(Enum):
    config = 'z_offset'
    parameters = 'z_offset_parameters'

    UNIFORM = 0  # choose uniform offset (in JSON as 'fiber_z/offset'... 0.0 for node centered about z bounds)
    RANDOM = 1  # max range of +/- 1/2 segment length (internodal length for MRG)


@unique
class MyelinationMode(Enum):
    config = 'myel'
    parameters = 'fiber_type_parameters'

    MYELINATED = True
    UNMYELINATED = False


@unique
class FiberGeometry(Enum):
    config = 'myel_fiber'

    NONE = None
    MRG_DISCRETE = "MRG_DISCRETE"
    MRG_INTERPOLATION = "MRG_INTERPOLATION"
    B_FIBER = "B_FIBER"
    C_FIBER = "C_FIBER"


@unique
class NeuronFiberFlags(Enum):
    NONE = None
    MRG_DISCRETE = "MRG_DISCRETE"
    MRG_INTERPOLATION = "MRG_INTERPOLATION"
    C_FIBER = "C_FIBER"


@unique
class MyelinatedSamplingType(Enum):

    DISCRETE = "discrete"
    INTERPOLATION = "interp"


@unique
class UnmyelinatedFiberType(Enum):
    config = 'unmyel_fiber'

    NONE = None
    SUNDT = 0
    TIGERHOLM = 1
    RATTAY = 2
    SCHILD = 3


# %% Waveforms

@unique
class WaveformMode(Enum):
    config = 'waveform'
    global_parameters = 'global'

    MONOPHASIC_PULSE_TRAIN = 0
    SINUSOID = 1
    BIPHASIC_FULL_DUTY = 2
    BIPHASIC_PULSE_TRAIN = 3
    BIPHASIC_PULSE_TRAIN_Q_BALANCED_UNEVEN_PW = 4
    EXPLICIT = 5


# %% NEURON Protocols

@unique
class NeuronRunMode(Enum):
    config = 'mode'

    ACTIVATION_THRESHOLD = 0
    BLOCK_THRESHOLD = 1
    FINITE_AMPLITUDES = 2


@unique
class SearchAmplitudeIncrementMode(Enum):
    config = 'mode'

    ABSOLUTE_INCREMENT = 0
    PERCENT_INCREMENT = 1


@unique
class TerminationCriteriaMode(Enum):
    config = 'mode'

    PERCENT_DIFFERENCE = 0
    ABSOLUTE_DIFFERENCE = 1


# %% Perineurium Impedance

@unique
class PerineuriumThicknessMode(Enum):
    config = 'ci_perineurium_thickness'
    parameters = 'ci_perineurium_thickness_parameters'

    GRINBERG_2008 = 0
    MEASURED = 3
    PIG_VN_INHOUSE_200523 = 4
    RAT_VN_INHOUSE_200601 = 5
    HUMAN_VN_INHOUSE_200601 = 6


@unique
class PerineuriumResistivityMode(Enum):
    config = 'rho_perineurium'

    RHO_WEERASURIYA = 'RHO_WEERASURIYA'
    MANUAL = 'MANUAL'


# %% Cuffs

@unique
class CuffInnerMode(Enum):
    config = 'cuff_inner'
    parameters = 'cuff_inner_parameters'

    CIRCLE = 0
    BOUNDING_BOX = 1


class CuffMode(Enum):
    config = 'cuff_mode'
    parameters = 'cuff_parameters'

    BIPOLAR_EMBEDDED_RIBBON = 0
    BIPOLAR_EXPOSED_WIRE = 1
    LIVANOVA = 2
    ENTEROMEDICS = 3
    IMTHERA = 4


class CuffShiftMode(Enum):
    config = 'cuff_shift'

    AUTO_ROTATION_MIN_CIRCLE_BOUNDARY = 0
    AUTO_ROTATION_TRACE_BOUNDARY = 1
    NONE = 2
    PURPLE = 3
    NAIVE_ROTATION_MIN_CIRCLE_BOUNDARY = 4  # purple
    NAIVE_ROTATION_TRACE_BOUNDARY = 5


# %% Templates

@unique
class TemplateMode(Enum):
    path = os.path.join('config', 'templates')
    ELECTRODE_INPUT = 'electrode_input.json'
    MORPHOLOGY = 'morphology.json'
