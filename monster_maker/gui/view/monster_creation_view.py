# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Jon\Desktop\monster_maker\monster_maker\gui\\view\qt_designer\monster_creation_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MonsterCreationView(object):
    def setupUi(self, MonsterCreationView):
        MonsterCreationView.setObjectName("MonsterCreationView")
        MonsterCreationView.resize(510, 432)
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
        self.fl_traits = QtWidgets.QFormLayout()
        self.fl_traits.setObjectName("fl_traits")
        self._lbl_name = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_name.setObjectName("_lbl_name")
        self.fl_traits.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._lbl_name)
        self._lbl_description = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_description.setObjectName("_lbl_description")
        self.fl_traits.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._lbl_description)
        self._lbl_habitat = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_habitat.setObjectName("_lbl_habitat")
        self.fl_traits.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._lbl_habitat)
        self.lineedit_habitat = QtWidgets.QLineEdit(MonsterCreationView)
        self.lineedit_habitat.setObjectName("lineedit_habitat")
        self.fl_traits.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineedit_habitat)
        self._lbl_treasure = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_treasure.setObjectName("_lbl_treasure")
        self.fl_traits.setWidget(3, QtWidgets.QFormLayout.LabelRole, self._lbl_treasure)
        self.lineedit_treasure = QtWidgets.QLineEdit(MonsterCreationView)
        self.lineedit_treasure.setObjectName("lineedit_treasure")
        self.fl_traits.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineedit_treasure)
        self._lbl_creature_type = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_creature_type.setObjectName("_lbl_creature_type")
        self.fl_traits.setWidget(4, QtWidgets.QFormLayout.LabelRole, self._lbl_creature_type)
        self.cb_creature_type = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_creature_type.setObjectName("cb_creature_type")
        self.fl_traits.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.cb_creature_type)
        self._lbl_alignment = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_alignment.setObjectName("_lbl_alignment")
        self.fl_traits.setWidget(5, QtWidgets.QFormLayout.LabelRole, self._lbl_alignment)
        self.cb_alignment = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_alignment.setObjectName("cb_alignment")
        self.fl_traits.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.cb_alignment)
        self._lbl_size = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_size.setObjectName("_lbl_size")
        self.fl_traits.setWidget(6, QtWidgets.QFormLayout.LabelRole, self._lbl_size)
        self.cb_size = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_size.setObjectName("cb_size")
        self.fl_traits.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.cb_size)
        self.hl_name = QtWidgets.QHBoxLayout()
        self.hl_name.setObjectName("hl_name")
        self.lineedit_name = QtWidgets.QLineEdit(MonsterCreationView)
        self.lineedit_name.setObjectName("lineedit_name")
        self.hl_name.addWidget(self.lineedit_name)
        self.btn_generate_names = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_generate_names.setObjectName("btn_generate_names")
        self.hl_name.addWidget(self.btn_generate_names)
        self.progressbar_name = QtWidgets.QProgressBar(MonsterCreationView)
        self.progressbar_name.setProperty("value", 24)
        self.progressbar_name.setObjectName("progressbar_name")
        self.hl_name.addWidget(self.progressbar_name)
        self.fl_traits.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.hl_name)
        self.hl_description = QtWidgets.QHBoxLayout()
        self.hl_description.setObjectName("hl_description")
        self.textedit_description = QtWidgets.QTextEdit(MonsterCreationView)
        self.textedit_description.setObjectName("textedit_description")
        self.hl_description.addWidget(self.textedit_description)
        self.btn_refine_description = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_refine_description.setObjectName("btn_refine_description")
        self.hl_description.addWidget(self.btn_refine_description)
        self.progressbar_description = QtWidgets.QProgressBar(MonsterCreationView)
        self.progressbar_description.setProperty("value", 24)
        self.progressbar_description.setObjectName("progressbar_description")
        self.hl_description.addWidget(self.progressbar_description)
        self.fl_traits.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.hl_description)
        self._lbl_skills = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_skills.setObjectName("_lbl_skills")
        self.fl_traits.setWidget(7, QtWidgets.QFormLayout.LabelRole, self._lbl_skills)
        self.hl_skills = QtWidgets.QHBoxLayout()
        self.hl_skills.setObjectName("hl_skills")
        self.cb_skills = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_skills.setObjectName("cb_skills")
        self.hl_skills.addWidget(self.cb_skills)
        self.btn_skills_proficient = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_skills_proficient.setObjectName("btn_skills_proficient")
        self.hl_skills.addWidget(self.btn_skills_proficient)
        self.btn_skills_expert = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_skills_expert.setObjectName("btn_skills_expert")
        self.hl_skills.addWidget(self.btn_skills_expert)
        self.fl_traits.setLayout(7, QtWidgets.QFormLayout.FieldRole, self.hl_skills)
        self._lbl_condition_immunities = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_condition_immunities.setObjectName("_lbl_condition_immunities")
        self.fl_traits.setWidget(8, QtWidgets.QFormLayout.LabelRole, self._lbl_condition_immunities)
        self.hl_conditions = QtWidgets.QHBoxLayout()
        self.hl_conditions.setObjectName("hl_conditions")
        self.cb_conditions = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_conditions.setObjectName("cb_conditions")
        self.hl_conditions.addWidget(self.cb_conditions)
        self.btn_condition_immune = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_condition_immune.setObjectName("btn_condition_immune")
        self.hl_conditions.addWidget(self.btn_condition_immune)
        self.fl_traits.setLayout(8, QtWidgets.QFormLayout.FieldRole, self.hl_conditions)
        self._lbl_encounter_difficulty = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_encounter_difficulty.setObjectName("_lbl_encounter_difficulty")
        self.fl_traits.setWidget(9, QtWidgets.QFormLayout.LabelRole, self._lbl_encounter_difficulty)
        self.cb_encounter_difficulty = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_encounter_difficulty.setObjectName("cb_encounter_difficulty")
        self.fl_traits.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.cb_encounter_difficulty)
        self._lbl_encounter_size = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_encounter_size.setObjectName("_lbl_encounter_size")
        self.fl_traits.setWidget(10, QtWidgets.QFormLayout.LabelRole, self._lbl_encounter_size)
        self.cb_encounter_size = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_encounter_size.setObjectName("cb_encounter_size")
        self.fl_traits.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.cb_encounter_size)
        self._lbl_languages = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_languages.setObjectName("_lbl_languages")
        self.fl_traits.setWidget(11, QtWidgets.QFormLayout.LabelRole, self._lbl_languages)
        self.hl_languages = QtWidgets.QHBoxLayout()
        self.hl_languages.setObjectName("hl_languages")
        self.cb_languages = QtWidgets.QComboBox(MonsterCreationView)
        self.cb_languages.setObjectName("cb_languages")
        self.hl_languages.addWidget(self.cb_languages)
        self.btn_add_language = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_add_language.setObjectName("btn_add_language")
        self.hl_languages.addWidget(self.btn_add_language)
        self.btn_remove_language = QtWidgets.QPushButton(MonsterCreationView)
        self.btn_remove_language.setObjectName("btn_remove_language")
        self.hl_languages.addWidget(self.btn_remove_language)
        self.fl_traits.setLayout(11, QtWidgets.QFormLayout.FieldRole, self.hl_languages)
        self._lbl_telepathy = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_telepathy.setObjectName("_lbl_telepathy")
        self.fl_traits.setWidget(12, QtWidgets.QFormLayout.LabelRole, self._lbl_telepathy)
        self.hl_telepathy = QtWidgets.QHBoxLayout()
        self.hl_telepathy.setObjectName("hl_telepathy")
        self.checkbox_telepathy = QtWidgets.QCheckBox(MonsterCreationView)
        self.checkbox_telepathy.setText("")
        self.checkbox_telepathy.setObjectName("checkbox_telepathy")
        self.hl_telepathy.addWidget(self.checkbox_telepathy)
        self._lbl_telepathy_range = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_telepathy_range.setObjectName("_lbl_telepathy_range")
        self.hl_telepathy.addWidget(self._lbl_telepathy_range)
        self.lineedit_telepathy_range = QtWidgets.QLineEdit(MonsterCreationView)
        self.lineedit_telepathy_range.setObjectName("lineedit_telepathy_range")
        self.hl_telepathy.addWidget(self.lineedit_telepathy_range)
        self._lbl_telepathy_ft = QtWidgets.QLabel(MonsterCreationView)
        self._lbl_telepathy_ft.setObjectName("_lbl_telepathy_ft")
        self.hl_telepathy.addWidget(self._lbl_telepathy_ft)
        self.fl_traits.setLayout(12, QtWidgets.QFormLayout.FieldRole, self.hl_telepathy)
        self.verticalLayout.addLayout(self.fl_traits)

        self.retranslateUi(MonsterCreationView)
        QtCore.QMetaObject.connectSlotsByName(MonsterCreationView)

    def retranslateUi(self, MonsterCreationView):
        _translate = QtCore.QCoreApplication.translate
        MonsterCreationView.setWindowTitle(_translate("MonsterCreationView", "Form"))
        self._lbl_title.setText(_translate("MonsterCreationView", "Create New Monster"))
        self._lbl_name.setText(_translate("MonsterCreationView", "Name:"))
        self._lbl_description.setText(_translate("MonsterCreationView", "Description:"))
        self._lbl_habitat.setText(_translate("MonsterCreationView", "Habitat:"))
        self._lbl_treasure.setText(_translate("MonsterCreationView", "Treasure:"))
        self._lbl_creature_type.setText(_translate("MonsterCreationView", "Creature Type:"))
        self._lbl_alignment.setText(_translate("MonsterCreationView", "Alignment:"))
        self._lbl_size.setText(_translate("MonsterCreationView", "Size:"))
        self.btn_generate_names.setText(_translate("MonsterCreationView", "Generate"))
        self.btn_refine_description.setText(_translate("MonsterCreationView", "Refine"))
        self._lbl_skills.setText(_translate("MonsterCreationView", "Skills:"))
        self.btn_skills_proficient.setText(_translate("MonsterCreationView", "Proficient"))
        self.btn_skills_expert.setText(_translate("MonsterCreationView", "Expert"))
        self._lbl_condition_immunities.setText(_translate("MonsterCreationView", "Condition Immunities:"))
        self.btn_condition_immune.setText(_translate("MonsterCreationView", "Immune"))
        self._lbl_encounter_difficulty.setText(_translate("MonsterCreationView", "Encounter Difficulty:"))
        self._lbl_encounter_size.setText(_translate("MonsterCreationView", "Encounter Size:"))
        self._lbl_languages.setText(_translate("MonsterCreationView", "Languages:"))
        self.btn_add_language.setText(_translate("MonsterCreationView", "Add"))
        self.btn_remove_language.setText(_translate("MonsterCreationView", "Remove"))
        self._lbl_telepathy.setText(_translate("MonsterCreationView", "Telepathy:"))
        self._lbl_telepathy_range.setText(_translate("MonsterCreationView", "Range:"))
        self._lbl_telepathy_ft.setText(_translate("MonsterCreationView", "ft."))
