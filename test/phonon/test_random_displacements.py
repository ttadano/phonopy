import unittest
import os
import numpy as np
from phonopy import Phonopy
from phonopy.interface.vasp import read_vasp
from phonopy.file_IO import parse_FORCE_SETS, parse_BORN
from phonopy.phonon.random_displacements import RandomDisplacements

data_dir = os.path.dirname(os.path.abspath(__file__))

disp_str = """-0.0514654  0.1115076  0.0011100
-0.1780910 -0.0973049  0.1698372
-0.1532055 -0.1685844  0.2696392
-0.1985800 -0.1314423 -0.0496898
-0.1080178 -0.1717647 -0.0204162
 0.0936793  0.0296741 -0.1511135
-0.3356941 -0.1459993 -0.0281809
-0.2976510  0.1502010 -0.2907214
-0.2334291 -0.1556119  0.0821270
-0.1293066 -0.0674755 -0.1257030
-0.4017851 -0.1158274  0.0385163
-0.3751805  0.2183430 -0.4037309
-0.1135429 -0.0615372 -0.1399313
-0.1850432  0.1352458 -0.2158535
-0.2585097  0.0631317 -0.0843370
-0.3165835  0.1223332 -0.1733457
-0.1742562 -0.1309926  0.1222215
 0.0640609 -0.0245728 -0.1738627
-0.3140855 -0.1136079 -0.0376838
-0.3160274  0.1858955 -0.3112977
 0.1140535  0.0223505 -0.1936938
-0.0413314  0.1457069 -0.2165871
-0.2690085  0.0958113 -0.1638003
-0.3147487  0.1233289 -0.1184777
-0.1877001 -0.1533800  0.2366920
-0.0560419 -0.1331006 -0.1575333
-0.3035009 -0.0885274  0.0330783
-0.3380943  0.2472368 -0.3767877
-0.1372640 -0.0561450 -0.1189917
-0.1928859  0.1598169 -0.2433005
-0.3312110  0.1267395 -0.3016184
-0.3193205  0.1798292 -0.1289612
 0.1265522 -0.1787818  0.0009789
 0.0639243 -0.0548810 -0.0227700
-0.0470768  0.1475875 -0.2789066
-0.0783960  0.1894551 -0.0046175
-0.2270308 -0.0833323 -0.2325597
-0.2341782  0.3991952 -0.0731757
-0.3140104  0.2323930 -0.1028991
-0.5137982  0.1798655  0.0336329
 0.1871071 -0.0143198  0.1109201
 0.0259593 -0.2209235  0.1097609
 0.0934036 -0.0544112 -0.1293274
 0.0348889  0.0155738 -0.0953390
 0.0243686 -0.2053247  0.0856274
-0.0469223 -0.1280702  0.0609982
-0.1300982  0.0464706 -0.2908150
-0.1562722  0.3817999 -0.0706285
 0.2520720 -0.0446607  0.1601216
 0.0748614 -0.1583794  0.0007053
 0.0950268  0.0511400 -0.2307183
 0.0185852  0.1263185 -0.1600272
 0.0455906 -0.1628427  0.0008357
-0.0648477 -0.0435683 -0.1238486
-0.2094037  0.0993982 -0.3790105
-0.2272393  0.2552084 -0.0348276
 0.2935021 -0.0194070  0.2240964
 0.0923349 -0.2410340  0.1113123
 0.1087797 -0.0745681 -0.1396408
 0.0224714  0.0611535 -0.1814881
-0.1036679 -0.1435858  0.0360042
-0.2067574 -0.1451977 -0.0743127
-0.2753820 -0.0162736 -0.3580231
-0.2856068  0.3571327 -0.1188627"""


randn_ii_str = """-1.7497654731  0.3426804033  1.1530358026 -0.2524360365  0.9813207870  0.5142188414
 0.2211796692 -1.0700433306 -0.1894958308  0.2550014443 -0.4580269855  0.4351634881
-0.5835950503  0.8168470717  0.6727208057 -0.1044111434 -0.5312803769  1.0297326851
-0.4381356227 -1.1183182463  1.6189816607  1.5416051745 -0.2518791392 -0.8424357383
 0.1845186906  0.9370822011  0.7310003438  1.3615561251 -0.3262380592  0.0556760149
 0.2223996086 -1.4432169952 -0.7563523056  0.8164540110  0.7504447615 -0.4559469275
 1.1896222680 -1.6906168264 -1.3563990489 -1.2324345139 -0.5444391617 -0.6681717368
 0.0073145632 -0.6129387355  1.2997480748 -1.7330956237 -0.9833100991  0.3575077532"""

randn_ij_str_1 = """-1.6135785028  1.4707138666 -1.1880175973 -0.5497461935 -0.9400461615 -0.8279323644
-0.8817983895  0.0186389495  0.2378446219  0.0135485486 -1.6355293994 -1.0442098777
-0.3317771351 -0.6892179781  2.0346075615 -0.5507144119  0.7504533303 -1.3069923391
 0.7788223993  0.4282328706  0.1088719899  0.0282836348 -0.5788258248 -1.1994511992
-0.0760234657  0.0039575940 -0.1850141109 -2.4871515352 -1.7046512058 -1.1362610068
 0.3173679759 -0.7524141777 -1.2963918072  0.0951394436 -0.4237150999 -1.1859835649
-1.5406160246  2.0467139685 -1.3969993450 -1.0971719846 -0.2387128693 -1.4290668984
 1.2962625864  0.9522756261 -1.2172541306 -0.1572651674 -1.5075851603  0.1078841308
 2.0747931679 -0.3432976822 -0.6166293717  0.7631836461  0.1929171918 -0.3484589307
 1.7036239881 -0.7221507701  1.0936866497 -0.2295177532 -0.0088986633 -0.5431980084
-2.0151887171 -0.0795405869  0.3010494638 -1.6848999617  0.2223908094 -0.6849217352
-0.5144298914 -0.2160601200  0.4223802204 -1.0940429310  1.2369078852 -0.2302846784"""

randn_ij_str_2 = """ 0.1088634678  0.5078095905 -0.8622273465  1.2494697427 -0.0796112459 -0.8897314813
 0.6130388817  0.7362052133  1.0269214394 -1.4321906111 -1.8411883002  0.3660932262
 0.5805733358 -1.1045230927  0.6901214702  0.6868900661 -1.5666875296  0.9049741215
-1.7059520057  0.3691639571  1.8765734270 -0.3769033502  1.8319360818  0.0030174340
-2.9733154741  0.0333172781 -0.2488886671 -0.4501764350  0.1324278011  0.0222139280
-0.3654619927 -1.2710230408  1.5861709384  0.6933906585 -1.9580812342 -0.1348013120
 0.9490047765 -0.0193975860  0.8945977058  0.7596931199 -1.4977203811 -1.1938859768
 0.7470556551  0.4296764359 -1.4150429209 -0.6407599230  0.7796263037 -0.4381209163
 2.2986539407 -0.1652095526  0.4662993684  0.2699872386 -0.3198310471 -1.1477415999
 0.7530621877 -1.6094388962  1.9432622634 -1.4474361123  0.1302484554  0.9493608647
-0.1262011837  1.9902736498  0.5229978045 -0.0163454028 -0.4158163358 -1.3585029368
-0.7044181997 -0.5913751211  0.7369951690  0.4358672525  1.7759935855  0.5130743788"""


class TestRandomDisplacements(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _get_phonon_NaCl(self):
        cell = read_vasp(os.path.join(data_dir, "..", "POSCAR_NaCl"))
        phonon = Phonopy(cell,
                         np.diag([2, 2, 2]),
                         primitive_matrix=[[0, 0.5, 0.5],
                                           [0.5, 0, 0.5],
                                           [0.5, 0.5, 0]])
        filename = os.path.join(data_dir, "..", "FORCE_SETS_NaCl")
        force_sets = parse_FORCE_SETS(filename=filename)
        phonon.set_displacement_dataset(force_sets)
        phonon.produce_force_constants()
        phonon.symmetrize_force_constants()
        filename_born = os.path.join(data_dir, "..", "BORN_NaCl")
        nac_params = parse_BORN(phonon.get_primitive(), filename=filename_born)
        phonon.set_nac_params(nac_params)
        return phonon

    def test_NaCl(self):
        """Test by fixed random numbers of np.random.normal

        randn_ii and randn_ij were created by

            randn_ii = np.random.normal(size=(N_ii, 1, num_band))
            randn_ij = np.random.normal(size=(N_ij, 2, 1, num_band)).

        numpy v1.16.4 (py37h6b0580a_0) on macOS installed from conda-forge
        was used.

        """

        phonon = self._get_phonon_NaCl()
        rd = RandomDisplacements(phonon.supercell,
                                 phonon.primitive,
                                 phonon.force_constants,
                                 cutoff_frequency=0.01)
        num_band = phonon.primitive.get_number_of_atoms() * 3
        N = int(np.rint(phonon.supercell.volume / phonon.primitive.volume))
        N_ij = N - len(rd.qpoints)
        N_ii = N - N_ij * 2
        shape_ii = (N_ii, 1, num_band)
        randn_ii = np.fromstring(randn_ii_str.replace('\n', ' '),
                                 dtype=float, sep=' ').reshape(shape_ii)
        shape_ij = (N_ij, 2, 1, num_band)
        randn_ij = np.zeros(shape_ij, dtype=float)
        randn_ij[:, 0, 0, :] = np.fromstring(
            randn_ij_str_1.replace('\n', ' '),
            dtype=float, sep=' ').reshape(N_ij, num_band)
        randn_ij[:, 1, 0, :] = np.fromstring(
            randn_ij_str_2.replace('\n', ' '),
            dtype=float, sep=' ').reshape(N_ij, num_band)

        rd.run(500, randn=(randn_ii, randn_ij))
        data = np.fromstring(disp_str.replace('\n', ' '), dtype=float, sep=' ')
        np.testing.assert_allclose(data, rd.u.ravel(), atol=1e-5)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestRandomDisplacements)
    unittest.TextTestRunner(verbosity=2).run(suite)
