# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Jon\Desktop\monster_maker\monster_forge\gui\\view\qt_designer\monster_creation_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MonsterCreationView(object):
    def setupUi(self, MonsterCreationView):
        MonsterCreationView.setObjectName("MonsterCreationView")
        MonsterCreationView.resize(468, 1130)
        self.verticalLayout = QtWidgets.QVBoxLayout(MonsterCreationView)
        self.verticalLayout.setObjectName("verticalLayout")
        self._lbl_title = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_title.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self._lbl_title.setFont(font)
        self._lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self._lbl_title.setObjectName("_lbl_title")
        self.verticalLayout.addWidget(self._lbl_title)
        self.progressbar_main = QtWidgets.QProgressBar(MonsterCreationView)
        self.progressbar_main.setProperty("value", 24)
        self.progressbar_main.setObjectName("progressbar_main")
        self.verticalLayout.addWidget(self.progressbar_main)
        self.gl_main = QtWidgets.QGridLayout()
        self.gl_main.setObjectName("gl_main")
        self.lineedit_name = QtWidgets.QLineEdit(MonsterCreationView)
        self.lineedit_name.setObjectName("lineedit_name")
        self.gl_main.addWidget(self.lineedit_name, 0, 1, 1, 1)
        self.btn_suggest_names = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_suggest_names.setObjectName("btn_suggest_names")
        self.gl_main.addWidget(self.btn_suggest_names, 0, 2, 1, 1)
        self._lbl_description = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_description.setObjectName("_lbl_description")
        self.gl_main.addWidget(self._lbl_description, 1, 0, 1, 1)
        self.btn_refine_description = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_refine_description.setObjectName("btn_refine_description")
        self.gl_main.addWidget(self.btn_refine_description, 1, 2, 1, 1)
        self._lbl_name = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_name.setObjectName("_lbl_name")
        self.gl_main.addWidget(self._lbl_name, 0, 0, 1, 1)
        self.textedit_description = QtWidgets.QTextEdit(MonsterCreationView)
        self.textedit_description.setObjectName("textedit_description")
        self.gl_main.addWidget(self.textedit_description, 1, 1, 1, 1)
        self._lbl_artwork = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_artwork.setObjectName("_lbl_artwork")
        self.gl_main.addWidget(self._lbl_artwork, 2, 0, 1, 1)
        self.lbl_artwork = QtWidgets.QLabel(MonsterCreationView)
        self.lbl_artwork.setText("")
        self.lbl_artwork.setObjectName("lbl_artwork")
        self.gl_main.addWidget(self.lbl_artwork, 2, 1, 1, 1)
        self.btn_generate_artwork = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_generate_artwork.setObjectName("btn_generate_artwork")
        self.gl_main.addWidget(self.btn_generate_artwork, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gl_main)
        self._hl_1 = QtWidgets.QFrame(MonsterCreationView)
        self._hl_1.setFrameShape(QtWidgets.QFrame.HLine)
        self._hl_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self._hl_1.setObjectName("_hl_1")
        self.verticalLayout.addWidget(self._hl_1)
        self.btn_generate_all = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_generate_all.setObjectName("btn_generate_all")
        self.verticalLayout.addWidget(self.btn_generate_all)
        self.progressbar_generate_all = QtWidgets.QProgressBar(MonsterCreationView)
        self.progressbar_generate_all.setProperty("value", 24)
        self.progressbar_generate_all.setObjectName("progressbar_generate_all")
        self.verticalLayout.addWidget(self.progressbar_generate_all)
        self._hl_2 = QtWidgets.QFrame(MonsterCreationView)
        self._hl_2.setFrameShape(QtWidgets.QFrame.HLine)
        self._hl_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self._hl_2.setObjectName("_hl_2")
        self.verticalLayout.addWidget(self._hl_2)
        self.gl_attributes = QtWidgets.QGridLayout()
        self.gl_attributes.setObjectName("gl_attributes")
        self._lbl_challenge_rating = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_challenge_rating.setObjectName("_lbl_challenge_rating")
        self.gl_attributes.addWidget(self._lbl_challenge_rating, 3, 0, 1, 1)
        self._lbl_ac = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_ac.setObjectName("_lbl_ac")
        self.gl_attributes.addWidget(self._lbl_ac, 4, 0, 1, 1)
        self.cb_alignment = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_alignment.setObjectName("cb_alignment")
        self.gl_attributes.addWidget(self.cb_alignment, 1, 1, 1, 1)
        self.btn_suggest_creature_type = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_suggest_creature_type.setObjectName("btn_suggest_creature_type")
        self.gl_attributes.addWidget(self.btn_suggest_creature_type, 0, 2, 1, 1)
        self._lbl_walk_ft = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_walk_ft.setObjectName("_lbl_walk_ft")
        self.gl_attributes.addWidget(self._lbl_walk_ft, 6, 2, 1, 1)
        self._lbl_fly_ft = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_fly_ft.setObjectName("_lbl_fly_ft")
        self.gl_attributes.addWidget(self._lbl_fly_ft, 8, 2, 1, 1)
        self.spinbox_walk_speed = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_walk_speed.setSingleStep(5)
        self.spinbox_walk_speed.setProperty("value", 30)
        self.spinbox_walk_speed.setObjectName("spinbox_walk_speed")
        self.gl_attributes.addWidget(self.spinbox_walk_speed, 6, 1, 1, 1)
        self.lineedit_challenge_rating = QtWidgets.QLineEdit(MonsterCreationView)
        self.lineedit_challenge_rating.setObjectName("lineedit_challenge_rating")
        self.gl_attributes.addWidget(self.lineedit_challenge_rating, 3, 1, 1, 1)
        self._lbl_fly_speed = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_fly_speed.setObjectName("_lbl_fly_speed")
        self.gl_attributes.addWidget(self._lbl_fly_speed, 8, 0, 1, 1)
        self.btn_suggest_size = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_suggest_size.setObjectName("btn_suggest_size")
        self.gl_attributes.addWidget(self.btn_suggest_size, 2, 2, 1, 1)
        self._lbl_swim_ft = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_swim_ft.setObjectName("_lbl_swim_ft")
        self.gl_attributes.addWidget(self._lbl_swim_ft, 7, 2, 1, 1)
        self.lineedit_hp = QtWidgets.QLineEdit(MonsterCreationView)
        self.lineedit_hp.setEnabled(False)
        self.lineedit_hp.setObjectName("lineedit_hp")
        self.gl_attributes.addWidget(self.lineedit_hp, 5, 1, 1, 1)
        self._lbl_climb_speed = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_climb_speed.setObjectName("_lbl_climb_speed")
        self.gl_attributes.addWidget(self._lbl_climb_speed, 9, 0, 1, 1)
        self.spinbox_swim_speed = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_swim_speed.setSingleStep(5)
        self.spinbox_swim_speed.setObjectName("spinbox_swim_speed")
        self.gl_attributes.addWidget(self.spinbox_swim_speed, 7, 1, 1, 1)
        self.spinbox_fly_speed = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_fly_speed.setSingleStep(5)
        self.spinbox_fly_speed.setObjectName("spinbox_fly_speed")
        self.gl_attributes.addWidget(self.spinbox_fly_speed, 8, 1, 1, 1)
        self._lbl_swim_speed = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_swim_speed.setObjectName("_lbl_swim_speed")
        self.gl_attributes.addWidget(self._lbl_swim_speed, 7, 0, 1, 1)
        self.spinbox_ac = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_ac.setEnabled(False)
        self.spinbox_ac.setMaximum(30)
        self.spinbox_ac.setProperty("value", 10)
        self.spinbox_ac.setObjectName("spinbox_ac")
        self.gl_attributes.addWidget(self.spinbox_ac, 4, 1, 1, 1)
        self._lbl_size = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_size.setObjectName("_lbl_size")
        self.gl_attributes.addWidget(self._lbl_size, 2, 0, 1, 1)
        self.lbl_per_monster_for_x_monsters = QtWidgets.QLabel(MonsterCreationView)
        self.lbl_per_monster_for_x_monsters.setObjectName("lbl_per_monster_for_x_monsters")
        self.gl_attributes.addWidget(self.lbl_per_monster_for_x_monsters, 3, 2, 1, 1)
        self._lbl_walk_speed = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_walk_speed.setObjectName("_lbl_walk_speed")
        self.gl_attributes.addWidget(self._lbl_walk_speed, 6, 0, 1, 1)
        self._lbl_alignment = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_alignment.setObjectName("_lbl_alignment")
        self.gl_attributes.addWidget(self._lbl_alignment, 1, 0, 1, 1)
        self.btn_suggest_alignment = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_suggest_alignment.setObjectName("btn_suggest_alignment")
        self.gl_attributes.addWidget(self.btn_suggest_alignment, 1, 2, 1, 1)
        self.cb_creature_type = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_creature_type.setObjectName("cb_creature_type")
        self.gl_attributes.addWidget(self.cb_creature_type, 0, 1, 1, 1)
        self.checkbox_ac_cr_tie = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_ac_cr_tie.setChecked(True)
        self.checkbox_ac_cr_tie.setObjectName("checkbox_ac_cr_tie")
        self.gl_attributes.addWidget(self.checkbox_ac_cr_tie, 4, 2, 1, 1)
        self.checkbox_hp_cr_tie = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_hp_cr_tie.setChecked(True)
        self.checkbox_hp_cr_tie.setObjectName("checkbox_hp_cr_tie")
        self.gl_attributes.addWidget(self.checkbox_hp_cr_tie, 5, 2, 1, 1)
        self.cb_size = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_size.setObjectName("cb_size")
        self.gl_attributes.addWidget(self.cb_size, 2, 1, 1, 1)
        self._lbl_hp = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_hp.setObjectName("_lbl_hp")
        self.gl_attributes.addWidget(self._lbl_hp, 5, 0, 1, 1)
        self._lbl_creature_type = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_creature_type.setObjectName("_lbl_creature_type")
        self.gl_attributes.addWidget(self._lbl_creature_type, 0, 0, 1, 1)
        self._lbl_burrow_speed = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_burrow_speed.setObjectName("_lbl_burrow_speed")
        self.gl_attributes.addWidget(self._lbl_burrow_speed, 10, 0, 1, 1)
        self.spinbox_burrow_speed = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_burrow_speed.setSingleStep(5)
        self.spinbox_burrow_speed.setObjectName("spinbox_burrow_speed")
        self.gl_attributes.addWidget(self.spinbox_burrow_speed, 10, 1, 1, 1)
        self.spinbox_climb_speed = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_climb_speed.setSingleStep(5)
        self.spinbox_climb_speed.setObjectName("spinbox_climb_speed")
        self.gl_attributes.addWidget(self.spinbox_climb_speed, 9, 1, 1, 1)
        self._lbl_climb_ft = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_climb_ft.setObjectName("_lbl_climb_ft")
        self.gl_attributes.addWidget(self._lbl_climb_ft, 9, 2, 1, 1)
        self._lbl_burrow_ft = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_burrow_ft.setObjectName("_lbl_burrow_ft")
        self.gl_attributes.addWidget(self._lbl_burrow_ft, 10, 2, 1, 1)
        self.verticalLayout.addLayout(self.gl_attributes)
        self._hl_3 = QtWidgets.QFrame(MonsterCreationView)
        self._hl_3.setFrameShape(QtWidgets.QFrame.HLine)
        self._hl_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self._hl_3.setObjectName("_hl_3")
        self.verticalLayout.addWidget(self._hl_3)
        self._lbl_encounter_details_title = QtWidgets.QLabel(MonsterCreationView)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self._lbl_encounter_details_title.setFont(font)
        self._lbl_encounter_details_title.setAlignment(QtCore.Qt.AlignCenter)
        self._lbl_encounter_details_title.setObjectName("_lbl_encounter_details_title")
        self.verticalLayout.addWidget(self._lbl_encounter_details_title)
        self.gl_encounter_details = QtWidgets.QGridLayout()
        self.gl_encounter_details.setObjectName("gl_encounter_details")
        self.cb_encounter_size = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_encounter_size.setObjectName("cb_encounter_size")
        self.gl_encounter_details.addWidget(self.cb_encounter_size, 0, 1, 1, 1)
        self._lbl_encounter_difficulty = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_encounter_difficulty.setObjectName("_lbl_encounter_difficulty")
        self.gl_encounter_details.addWidget(self._lbl_encounter_difficulty, 1, 0, 1, 1)
        self.spinbox_avg_party_lvl = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_avg_party_lvl.setProperty("value", 1)
        self.spinbox_avg_party_lvl.setObjectName("spinbox_avg_party_lvl")
        self.gl_encounter_details.addWidget(self.spinbox_avg_party_lvl, 2, 1, 1, 1)
        self._lbl_avg_party_lvl = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_avg_party_lvl.setObjectName("_lbl_avg_party_lvl")
        self.gl_encounter_details.addWidget(self._lbl_avg_party_lvl, 2, 0, 1, 1)
        self.cb_encounter_difficulty = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_encounter_difficulty.setObjectName("cb_encounter_difficulty")
        self.gl_encounter_details.addWidget(self.cb_encounter_difficulty, 1, 1, 1, 1)
        self._lbl_encounter_size = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_encounter_size.setObjectName("_lbl_encounter_size")
        self.gl_encounter_details.addWidget(self._lbl_encounter_size, 0, 0, 1, 1)
        self._lbl_num_pcs = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_num_pcs.setObjectName("_lbl_num_pcs")
        self.gl_encounter_details.addWidget(self._lbl_num_pcs, 3, 0, 1, 1)
        self.spinbox_num_pcs = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_num_pcs.setProperty("value", 1)
        self.spinbox_num_pcs.setObjectName("spinbox_num_pcs")
        self.gl_encounter_details.addWidget(self.spinbox_num_pcs, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gl_encounter_details)
        self._hl_4 = QtWidgets.QFrame(MonsterCreationView)
        self._hl_4.setFrameShape(QtWidgets.QFrame.HLine)
        self._hl_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self._hl_4.setObjectName("_hl_4")
        self.verticalLayout.addWidget(self._hl_4)
        self._lbl_ability_scores = QtWidgets.QLabel(MonsterCreationView)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self._lbl_ability_scores.setFont(font)
        self._lbl_ability_scores.setAlignment(QtCore.Qt.AlignCenter)
        self._lbl_ability_scores.setObjectName("_lbl_ability_scores")
        self.verticalLayout.addWidget(self._lbl_ability_scores)
        self.btn_suggest_ability_scores = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_suggest_ability_scores.setObjectName("btn_suggest_ability_scores")
        self.verticalLayout.addWidget(self.btn_suggest_ability_scores)
        self.gl_ability_scores = QtWidgets.QGridLayout()
        self.gl_ability_scores.setObjectName("gl_ability_scores")
        self._lbl_dex = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_dex.setObjectName("_lbl_dex")
        self.gl_ability_scores.addWidget(self._lbl_dex, 0, 3, 1, 1)
        self.spinbox_con = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_con.setProperty("value", 10)
        self.spinbox_con.setObjectName("spinbox_con")
        self.gl_ability_scores.addWidget(self.spinbox_con, 0, 7, 1, 1)
        self._lbl_int = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_int.setObjectName("_lbl_int")
        self.gl_ability_scores.addWidget(self._lbl_int, 1, 0, 1, 1)
        self.spinbox_str = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_str.setProperty("value", 10)
        self.spinbox_str.setObjectName("spinbox_str")
        self.gl_ability_scores.addWidget(self.spinbox_str, 0, 1, 1, 1)
        self._lbl_wis = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_wis.setObjectName("_lbl_wis")
        self.gl_ability_scores.addWidget(self._lbl_wis, 1, 3, 1, 1)
        self.checkbox_prof_int_st = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_prof_int_st.setObjectName("checkbox_prof_int_st")
        self.gl_ability_scores.addWidget(self.checkbox_prof_int_st, 1, 2, 1, 1)
        self.spinbox_cha = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_cha.setProperty("value", 10)
        self.spinbox_cha.setObjectName("spinbox_cha")
        self.gl_ability_scores.addWidget(self.spinbox_cha, 1, 7, 1, 1)
        self._lbl_con = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_con.setObjectName("_lbl_con")
        self.gl_ability_scores.addWidget(self._lbl_con, 0, 6, 1, 1)
        self.spinbox_wis = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_wis.setProperty("value", 10)
        self.spinbox_wis.setObjectName("spinbox_wis")
        self.gl_ability_scores.addWidget(self.spinbox_wis, 1, 4, 1, 1)
        self.checkbox_prof_str_st = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_prof_str_st.setObjectName("checkbox_prof_str_st")
        self.gl_ability_scores.addWidget(self.checkbox_prof_str_st, 0, 2, 1, 1)
        self.checkbox_prof_wis_st = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_prof_wis_st.setObjectName("checkbox_prof_wis_st")
        self.gl_ability_scores.addWidget(self.checkbox_prof_wis_st, 1, 5, 1, 1)
        self._lbl_str = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_str.setObjectName("_lbl_str")
        self.gl_ability_scores.addWidget(self._lbl_str, 0, 0, 1, 1)
        self.spinbox_int = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_int.setProperty("value", 10)
        self.spinbox_int.setObjectName("spinbox_int")
        self.gl_ability_scores.addWidget(self.spinbox_int, 1, 1, 1, 1)
        self._lbl_cha = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_cha.setObjectName("_lbl_cha")
        self.gl_ability_scores.addWidget(self._lbl_cha, 1, 6, 1, 1)
        self.spinbox_dex = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_dex.setProperty("value", 10)
        self.spinbox_dex.setObjectName("spinbox_dex")
        self.gl_ability_scores.addWidget(self.spinbox_dex, 0, 4, 1, 1)
        self.checkbox_prof_dex_st = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_prof_dex_st.setObjectName("checkbox_prof_dex_st")
        self.gl_ability_scores.addWidget(self.checkbox_prof_dex_st, 0, 5, 1, 1)
        self.checkbox_prof_con_st = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_prof_con_st.setObjectName("checkbox_prof_con_st")
        self.gl_ability_scores.addWidget(self.checkbox_prof_con_st, 0, 8, 1, 1)
        self.checkbox_prof_cha_st = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_prof_cha_st.setObjectName("checkbox_prof_cha_st")
        self.gl_ability_scores.addWidget(self.checkbox_prof_cha_st, 1, 8, 1, 1)
        self.verticalLayout.addLayout(self.gl_ability_scores)
        self.line = QtWidgets.QFrame(MonsterCreationView)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gl_skills = QtWidgets.QGridLayout()
        self.gl_skills.setObjectName("gl_skills")
        self.btn_expert_skill = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_expert_skill.setObjectName("btn_expert_skill")
        self.gl_skills.addWidget(self.btn_expert_skill, 0, 3, 1, 1)
        self.cb_damage = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_damage.setObjectName("cb_damage")
        self.gl_skills.addWidget(self.cb_damage, 1, 1, 1, 1)
        self.btn_remove_condition = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_remove_condition.setObjectName("btn_remove_condition")
        self.gl_skills.addWidget(self.btn_remove_condition, 2, 5, 1, 1)
        self.btn_immune_damage = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_immune_damage.setObjectName("btn_immune_damage")
        self.gl_skills.addWidget(self.btn_immune_damage, 1, 3, 1, 1)
        self.listview_damage = QtWidgets.QListWidget(MonsterCreationView)
        self.listview_damage.setObjectName("listview_damage")
        self.gl_skills.addWidget(self.listview_damage, 1, 4, 1, 1)
        self.btn_immune_condition = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_immune_condition.setObjectName("btn_immune_condition")
        self.gl_skills.addWidget(self.btn_immune_condition, 2, 2, 1, 1)
        self._lbl_languages = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_languages.setObjectName("_lbl_languages")
        self.gl_skills.addWidget(self._lbl_languages, 3, 0, 1, 1)
        self.listview_conditions = QtWidgets.QListWidget(MonsterCreationView)
        self.listview_conditions.setObjectName("listview_conditions")
        self.gl_skills.addWidget(self.listview_conditions, 2, 4, 1, 1)
        self._lbl_telepathy = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_telepathy.setObjectName("_lbl_telepathy")
        self.gl_skills.addWidget(self._lbl_telepathy, 5, 0, 1, 1)
        self._lbl_conditions = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_conditions.setObjectName("_lbl_conditions")
        self.gl_skills.addWidget(self._lbl_conditions, 2, 0, 1, 1)
        self.btn_all_languages = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_all_languages.setObjectName("btn_all_languages")
        self.gl_skills.addWidget(self.btn_all_languages, 3, 3, 1, 1)
        self.checkbox_telepathy = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_telepathy.setText("")
        self.checkbox_telepathy.setObjectName("checkbox_telepathy")
        self.gl_skills.addWidget(self.checkbox_telepathy, 5, 1, 1, 1)
        self.lineedit_telepathy_range = QtWidgets.QLineEdit(MonsterCreationView)
        self.lineedit_telepathy_range.setObjectName("lineedit_telepathy_range")
        self.gl_skills.addWidget(self.lineedit_telepathy_range, 5, 3, 1, 1)
        self.btn_remove_skill = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_remove_skill.setObjectName("btn_remove_skill")
        self.gl_skills.addWidget(self.btn_remove_skill, 0, 5, 1, 1)
        self._lbl_ft = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_ft.setObjectName("_lbl_ft")
        self.gl_skills.addWidget(self._lbl_ft, 5, 4, 1, 1)
        self.btn_resistant_damage = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_resistant_damage.setObjectName("btn_resistant_damage")
        self.gl_skills.addWidget(self.btn_resistant_damage, 1, 2, 1, 1)
        self.btn_remove_damage = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_remove_damage.setObjectName("btn_remove_damage")
        self.gl_skills.addWidget(self.btn_remove_damage, 1, 5, 1, 1)
        self.btn_add_language = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_add_language.setObjectName("btn_add_language")
        self.gl_skills.addWidget(self.btn_add_language, 3, 2, 1, 1)
        self.cb_languages = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_languages.setObjectName("cb_languages")
        self.gl_skills.addWidget(self.cb_languages, 3, 1, 1, 1)
        self.listview_skills = QtWidgets.QListWidget(MonsterCreationView)
        self.listview_skills.setObjectName("listview_skills")
        self.gl_skills.addWidget(self.listview_skills, 0, 4, 1, 1)
        self.cb_skills = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_skills.setObjectName("cb_skills")
        self.gl_skills.addWidget(self.cb_skills, 0, 1, 1, 1)
        self.btn_remove_language = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_remove_language.setObjectName("btn_remove_language")
        self.gl_skills.addWidget(self.btn_remove_language, 3, 5, 1, 1)
        self.btn_proficient_skill = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_proficient_skill.setObjectName("btn_proficient_skill")
        self.gl_skills.addWidget(self.btn_proficient_skill, 0, 2, 1, 1)
        self._lbl_dmg = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_dmg.setObjectName("_lbl_dmg")
        self.gl_skills.addWidget(self._lbl_dmg, 1, 0, 1, 1)
        self.listview_languages = QtWidgets.QListWidget(MonsterCreationView)
        self.listview_languages.setObjectName("listview_languages")
        self.gl_skills.addWidget(self.listview_languages, 3, 4, 1, 1)
        self._lbl_range = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_range.setObjectName("_lbl_range")
        self.gl_skills.addWidget(self._lbl_range, 5, 2, 1, 1)
        self.cb_conditions = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_conditions.setObjectName("cb_conditions")
        self.gl_skills.addWidget(self.cb_conditions, 2, 1, 1, 1)
        self._lbl_skills = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_skills.setObjectName("_lbl_skills")
        self.gl_skills.addWidget(self._lbl_skills, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(MonsterCreationView)
        self.label.setObjectName("label")
        self.gl_skills.addWidget(self.label, 4, 0, 1, 1)
        self.cb_senses = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_senses.setObjectName("cb_senses")
        self.gl_skills.addWidget(self.cb_senses, 4, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinbox_sense_range = QtWidgets.QSpinBox(MonsterCreationView)
        self.spinbox_sense_range.setObjectName("spinbox_sense_range")
        self.horizontalLayout.addWidget(self.spinbox_sense_range)
        self._lbl_sense_range_ft = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_sense_range_ft.setObjectName("_lbl_sense_range_ft")
        self.horizontalLayout.addWidget(self._lbl_sense_range_ft)
        self.gl_skills.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.btn_add_sense = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_add_sense.setObjectName("btn_add_sense")
        self.gl_skills.addWidget(self.btn_add_sense, 4, 3, 1, 1)
        self.listview_senses = QtWidgets.QListWidget(MonsterCreationView)
        self.listview_senses.setObjectName("listview_senses")
        self.gl_skills.addWidget(self.listview_senses, 4, 4, 1, 1)
        self.btn_remove_sense = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_remove_sense.setObjectName("btn_remove_sense")
        self.gl_skills.addWidget(self.btn_remove_sense, 4, 5, 1, 1)
        self.verticalLayout.addLayout(self.gl_skills)
        self.line_2 = QtWidgets.QFrame(MonsterCreationView)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.btn_generate_markdown = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_generate_markdown.setObjectName("btn_generate_markdown")
        self.verticalLayout.addWidget(self.btn_generate_markdown)

        self.retranslateUi(MonsterCreationView)
        QtCore.QMetaObject.connectSlotsByName(MonsterCreationView)

    def retranslateUi(self, MonsterCreationView):
        _translate = QtCore.QCoreApplication.translate
        MonsterCreationView.setWindowTitle(_translate("MonsterCreationView", "Form"))
        self._lbl_title.setText(_translate("MonsterCreationView", "Create New Monster"))
        self.btn_suggest_names.setText(_translate("MonsterCreationView", "Suggest"))
        self._lbl_description.setText(_translate("MonsterCreationView", "Description:"))
        self.btn_refine_description.setText(_translate("MonsterCreationView", "Refine"))
        self._lbl_name.setText(_translate("MonsterCreationView", "Name:"))
        self._lbl_artwork.setText(_translate("MonsterCreationView", "Artwork:"))
        self.btn_generate_artwork.setText(_translate("MonsterCreationView", "Generate"))
        self.btn_generate_all.setText(_translate("MonsterCreationView", "Generate All"))
        self._lbl_challenge_rating.setText(_translate("MonsterCreationView", "Challenge Rating:"))
        self._lbl_ac.setText(_translate("MonsterCreationView", "AC:"))
        self.btn_suggest_creature_type.setText(_translate("MonsterCreationView", "Suggest"))
        self._lbl_walk_ft.setText(_translate("MonsterCreationView", "ft."))
        self._lbl_fly_ft.setText(_translate("MonsterCreationView", "ft."))
        self._lbl_fly_speed.setText(_translate("MonsterCreationView", "Fly Speed:"))
        self.btn_suggest_size.setText(_translate("MonsterCreationView", "Suggest"))
        self._lbl_swim_ft.setText(_translate("MonsterCreationView", "ft."))
        self._lbl_climb_speed.setText(_translate("MonsterCreationView", "Climb Speed:"))
        self._lbl_swim_speed.setText(_translate("MonsterCreationView", "Swim Speed:"))
        self._lbl_size.setText(_translate("MonsterCreationView", "Size:"))
        self.lbl_per_monster_for_x_monsters.setText(_translate("MonsterCreationView", "per monster, for x monsters"))
        self._lbl_walk_speed.setText(_translate("MonsterCreationView", "Walk Speed:"))
        self._lbl_alignment.setText(_translate("MonsterCreationView", "Alignment:"))
        self.btn_suggest_alignment.setText(_translate("MonsterCreationView", "Suggest"))
        self.checkbox_ac_cr_tie.setText(_translate("MonsterCreationView", "Tie to Challenge Rating"))
        self.checkbox_hp_cr_tie.setText(_translate("MonsterCreationView", "Tie to Challenge Rating"))
        self._lbl_hp.setText(_translate("MonsterCreationView", "HP:"))
        self._lbl_creature_type.setText(_translate("MonsterCreationView", "Creature Type:"))
        self._lbl_burrow_speed.setText(_translate("MonsterCreationView", "Burrow Speed:"))
        self._lbl_climb_ft.setText(_translate("MonsterCreationView", "ft."))
        self._lbl_burrow_ft.setText(_translate("MonsterCreationView", "ft."))
        self._lbl_encounter_details_title.setText(_translate("MonsterCreationView", "Encounter Details:"))
        self._lbl_encounter_difficulty.setText(_translate("MonsterCreationView", "Encounter Difficulty:"))
        self._lbl_avg_party_lvl.setText(_translate("MonsterCreationView", "Average Party Level:"))
        self._lbl_encounter_size.setText(_translate("MonsterCreationView", "Encounter Size:"))
        self._lbl_num_pcs.setText(_translate("MonsterCreationView", "Number of Player Characters:"))
        self._lbl_ability_scores.setText(_translate("MonsterCreationView", "Ability Scores"))
        self.btn_suggest_ability_scores.setText(_translate("MonsterCreationView", "Suggest"))
        self._lbl_dex.setText(_translate("MonsterCreationView", "Dex:"))
        self._lbl_int.setText(_translate("MonsterCreationView", "Int:"))
        self._lbl_wis.setText(_translate("MonsterCreationView", "Wis:"))
        self.checkbox_prof_int_st.setText(_translate("MonsterCreationView", "Proficient"))
        self._lbl_con.setText(_translate("MonsterCreationView", "Con:"))
        self.checkbox_prof_str_st.setText(_translate("MonsterCreationView", "Proficient"))
        self.checkbox_prof_wis_st.setText(_translate("MonsterCreationView", "Proficient"))
        self._lbl_str.setText(_translate("MonsterCreationView", "Str:"))
        self._lbl_cha.setText(_translate("MonsterCreationView", "Cha:"))
        self.checkbox_prof_dex_st.setText(_translate("MonsterCreationView", "Proficient"))
        self.checkbox_prof_con_st.setText(_translate("MonsterCreationView", "Proficient"))
        self.checkbox_prof_cha_st.setText(_translate("MonsterCreationView", "Proficient"))
        self.btn_expert_skill.setText(_translate("MonsterCreationView", "Expert"))
        self.btn_remove_condition.setText(_translate("MonsterCreationView", "Remove"))
        self.btn_immune_damage.setText(_translate("MonsterCreationView", "Immune"))
        self.btn_immune_condition.setText(_translate("MonsterCreationView", "Immune"))
        self._lbl_languages.setText(_translate("MonsterCreationView", "Languages:"))
        self._lbl_telepathy.setText(_translate("MonsterCreationView", "Telepathy:"))
        self._lbl_conditions.setText(_translate("MonsterCreationView", "Conditions:"))
        self.btn_all_languages.setText(_translate("MonsterCreationView", "All"))
        self.btn_remove_skill.setText(_translate("MonsterCreationView", "Remove"))
        self._lbl_ft.setText(_translate("MonsterCreationView", "ft."))
        self.btn_resistant_damage.setText(_translate("MonsterCreationView", "Resistant"))
        self.btn_remove_damage.setText(_translate("MonsterCreationView", "Remove"))
        self.btn_add_language.setText(_translate("MonsterCreationView", "Add"))
        self.btn_remove_language.setText(_translate("MonsterCreationView", "Remove"))
        self.btn_proficient_skill.setText(_translate("MonsterCreationView", "Proficient"))
        self._lbl_dmg.setText(_translate("MonsterCreationView", "Damage:"))
        self._lbl_range.setText(_translate("MonsterCreationView", "Range:"))
        self._lbl_skills.setText(_translate("MonsterCreationView", "Skills:"))
        self.label.setText(_translate("MonsterCreationView", "Senses:"))
        self._lbl_sense_range_ft.setText(_translate("MonsterCreationView", "ft."))
        self.btn_add_sense.setText(_translate("MonsterCreationView", "Add"))
        self.btn_remove_sense.setText(_translate("MonsterCreationView", "Remove"))
        self.btn_generate_markdown.setText(_translate("MonsterCreationView", "Generate Markdown"))
