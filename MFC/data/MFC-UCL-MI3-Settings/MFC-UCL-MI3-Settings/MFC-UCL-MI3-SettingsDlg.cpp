// MFC-UCL-MI3-SettingsDlg.cpp : IMPLEMENTATION FILE
// Author: Anelia Gaydardzhieva
#include "pch.h"
#include "math.h"
#include "framework.h"
#include "MFC-UCL-MI3-Settings.h"
#include "MFC-UCL-MI3-SettingsDlg.h"
#include "afxdialogex.h"
#include <Windows.h>
#include <filesystem>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include "../packages/nlohmann.json.3.10.5/build/native/include/nlohmann/json.hpp"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

// define json library
using json = nlohmann::json;
using namespace std;

// define global variables
string globalMode;
string globalCurrentMode;
bool globalSpeech;
int globalCameraNr;
bool globalShowFPS;
bool globalLowLight;
int globalMouseNose;
int globalMouseEye;
int globalBoundBoxNose;
double globalSmile;
double globalFishFace;
double globalRaisedEyebrows;
double globalOpenMounth;

const LPCTSTR facialValues[6] = { L"Left Click", L"Right Click", L"Double Click", L"Left Hold/Release", L"Right Hold/Release", L"On/Off Eye Gaze"};
const string facialConstants[6] = {"_left_click", "_right_click", "_double_click", "_left_press_hold_release", "_right_press_hold_release", "_on_off_eye_gaze"};

// Define grids
#define GRID_NOSE_SPEECH "nose_grid_speech"
#define GRID_EYES_SPEECH "eye_grid_speech"
#define GRID_NOSE_FACIAL "nose_grid_facial"
#define GRID_EYES_FACIAL "eye_grid_facial"

// Define MODE Values
#define MODE_NOSE "Nose"
#define MODE_EYES "Eyes"
#define METHOD_FACIAL "Facial"
#define METHOD_SPEECH "Speech"

// parameters
#define MAX_CAMERA_INDEX 9

json globalModesData;

// CMFCUCLMI3SettingsDlg Dialog - MFC VARIABLES
CMFCUCLMI3SettingsDlg::CMFCUCLMI3SettingsDlg(CWnd* pParent) : CDialogEx(IDD_MFCUCLMI3SETTINGS_DIALOG, pParent){
	//UCL LOGO ICON
	m_hIcon = AfxGetApp()->LoadIcon(IDI_ICON1);
	// uncomment below for the MFC default logo (and comment the line above)
	//m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CMFCUCLMI3SettingsDlg::DoDataExchange(CDataExchange* pDX){
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_DEFAULTCAMERA_COMBO, m_camera);
	DDX_Control(pDX, IDC_NOSESPEED_SLIDER, m_noseMouseSpeed);
	// DDX_Control(pDX, IDC_EDIT3, m_cameraValue);
	DDX_Control(pDX, IDC_NOSESPEED_COUNTER, m_noseMouseSpeedValue);
	DDX_Control(pDX, IDC_EYEMOUSE_SPEED_SLIDER, m_eyesMouseSpeed);
	DDX_Control(pDX, IDC_EYEMOUSE_SPEED_COUNTER, m_eyesMouseSpeedValue);
	DDX_Control(pDX, IDC_FPS_BUTTON, m_showFPS);
	DDX_Control(pDX, IDC_LOW_LIGHT_BUTTON, m_lowLightOn);
	DDX_Control(pDX, IDC_SMILE_COMBO, m_smile);
	DDX_Control(pDX, IDC_FISH_FACE_COMBO, m_fishFace);
	DDX_Control(pDX, IDC_RAISED_EYEBROWS_COMBO, m_raisedEyebrows);
	DDX_Control(pDX, IDC_OPEN_MOUTH_COMBO, m_openMouth);
	DDX_Control(pDX, IDC_NOSE_BUTTON, m_modeNose);
	DDX_Control(pDX, IDC_EYES_BUTTON, m_modeEyes);
	DDX_Control(pDX, IDC_FACIAL_BUTTON, m_methodFacial);
	DDX_Control(pDX, IDC_SPEECH_BUTTON, m_methodSpeech);
	DDX_Control(pDX, IDC_ROTATE_HEAD_RIGHT_COMBO, m_rotationRight);
	DDX_Control(pDX, IDC_ROTATE_HEAD_LEFT_COMBO, m_rotationLeft);
	DDX_Control(pDX, IDC_NOSEDISTANCE_SLIDER, m_noseBoxBond);
	DDX_Control(pDX, IDC_NOSEDISTANCE_COUNTER, m_noseBoxBondValue);
}

BEGIN_MESSAGE_MAP(CMFCUCLMI3SettingsDlg, CDialogEx)
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BUTTON_ABOUT, &CMFCUCLMI3SettingsDlg::ShowAbout)
	ON_BN_CLICKED(IDOK, &CMFCUCLMI3SettingsDlg::Save)
	ON_BN_CLICKED(IDC_BUTTON_HELP, &CMFCUCLMI3SettingsDlg::ShowHelp)
	ON_WM_HSCROLL()
	ON_WM_HSCROLL()
	ON_BN_CLICKED(IDC_FPS_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateShowFPS)
	ON_BN_CLICKED(IDC_LOW_LIGHT_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateLowLight)
	ON_BN_CLICKED(IDC_NOSE_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateModeNose)
	ON_BN_CLICKED(IDC_EYES_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateModeEyes)
	ON_BN_CLICKED(IDC_FACIAL_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateMethodFacial)
	ON_BN_CLICKED(IDC_SPEECH_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateMethodSpeech)
    ON_BN_CLICKED(IDC_BUTTON_INFO_MODE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMode)
    ON_BN_CLICKED(IDC_BUTTON_INFO_METHOD, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMethod)
    ON_BN_CLICKED(IDC_BUTTON_INFO_FPS, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFps)
    ON_BN_CLICKED(IDC_BUTTON_INFO_LIGHT, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoLight)
    ON_BN_CLICKED(IDC_BUTTON_INFO_CAMERA, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCamera)
    ON_BN_CLICKED(IDC_BUTTON_INFO_NOSE_SPEED, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoNoseMouse)
    ON_BN_CLICKED(IDC_BUTTON_INFO_NOSE_DISTANCE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoNoseboxBound)
    ON_BN_CLICKED(IDC_BUTTON_INFO_EYES_MOUSE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoEyesMouse)
    ON_BN_CLICKED(IDC_BUTTON_INFO_SMILE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSmile)
    ON_BN_CLICKED(IDC_BUTTON_INFO_FISHFACE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFishface)
    ON_BN_CLICKED(IDC_BUTTON_INFO_EYEBROWS, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoEyebrows)
    ON_BN_CLICKED(IDC_BUTTON_INFO_OPEN_MOUTH, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoOpenMouth)
    ON_BN_CLICKED(IDC_BUTTON_INFO_ROTATE_HEAD_LEFT, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoRotateHeadLeft)
    ON_BN_CLICKED(IDC_BUTTON_INFO_ROTATE_HEAD_RIGHT, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoRotateHeadRight)
	ON_CBN_SELCHANGE(IDC_DEFAULTCAMERA_COMBO, &CMFCUCLMI3SettingsDlg::OnCbnSelchangeDefaultcameraCombo)
	ON_BN_CLICKED(IDCANCEL, &CMFCUCLMI3SettingsDlg::OnBnClickedCancel)
END_MESSAGE_MAP()

// drag window cursor
HCURSOR CMFCUCLMI3SettingsDlg::OnQueryDragIcon() {
	return static_cast<HCURSOR>(m_hIcon);
}

// Paint
void CMFCUCLMI3SettingsDlg::OnPaint() {
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting
		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);
		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;
		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}


// Init
BOOL CMFCUCLMI3SettingsDlg::OnInitDialog(){
	CDialogEx::OnInitDialog();

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	//SetIcon(m_hIcon, FALSE);		// Set small icon


	// CONFIG data
	wstring pathConfigS = L"data\\config.json";
	LPCWSTR pathConfig = pathConfigS.c_str();

	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));

	json myjson_config = json::parse(content_config);
	auto& general = myjson_config["general"];
	auto& modules = myjson_config["modules"];
	auto& events = myjson_config["events"];

	// JSON MODES PATH
	wstring pathModesS = L"data\\mode_controller.json";
	LPCWSTR pathModes = pathModesS.c_str();

	ifstream ifs_modes(pathModes);
	string content_modes((istreambuf_iterator<char>(ifs_modes)), (istreambuf_iterator<char>()));

	json myjson_modes = json::parse(content_modes);
	auto& current_mode = myjson_modes["current_mode"];
	
	// Set mode data
	globalCurrentMode = current_mode;
	globalModesData = myjson_modes["modes"];
	auto& modes =	globalModesData[globalCurrentMode];
	// Mode
	m_modeNose.SetCheck(globalCurrentMode == GRID_NOSE_FACIAL || globalCurrentMode == GRID_NOSE_SPEECH);
	m_modeEyes.SetCheck(globalCurrentMode == GRID_EYES_FACIAL || globalCurrentMode == GRID_EYES_SPEECH);
	// Method
	m_methodFacial.SetCheck(globalCurrentMode == GRID_NOSE_FACIAL || globalCurrentMode == GRID_EYES_FACIAL);
	m_methodSpeech.SetCheck(globalCurrentMode == GRID_NOSE_SPEECH || globalCurrentMode == GRID_EYES_SPEECH);
	// Facial Switches
	m_smile.SetCurSel(0);
	m_fishFace.SetCurSel(0);
	m_raisedEyebrows.SetCurSel(0);
	m_openMouth.SetCurSel(0);
	m_rotationLeft.SetCurSel(0);
	m_rotationRight.SetCurSel(0);

	if (globalCurrentMode == GRID_NOSE_FACIAL || globalCurrentMode == GRID_EYES_FACIAL) {
		int n = (globalCurrentMode == GRID_NOSE_FACIAL) ? 5 : 6;

		for (int i = 0; i < n; i++) m_smile.AddString(facialValues[i]);
		for (int i = 0; i < n; i++) m_fishFace.AddString(facialValues[i]);
		for (int i = 0; i < n; i++) m_raisedEyebrows.AddString(facialValues[i]);
		for (int i = 0; i < n; i++) m_openMouth.AddString(facialValues[i]);
		for (int i = 0; i < n; i++) m_rotationLeft.AddString(facialValues[i]);
		for (int i = 0; i < n; i++) m_rotationRight.AddString(facialValues[i]);

		for (auto& el : modes.items()) {
			for (int i = 0; i < n; i++) if (el.value() == ("head_smile" + facialConstants[i])) m_smile.SetCurSel(i + 1);
			for (int i = 0; i < n; i++) if (el.value() == ("head_fishface" + facialConstants[i])) m_fishFace.SetCurSel(i + 1);
			for (int i = 0; i < n; i++) if (el.value() == ("head_raise_eyebrows" + facialConstants[i])) m_raisedEyebrows.SetCurSel(i + 1);
			for (int i = 0; i < n; i++) if (el.value() == ("head_open_mouth" + facialConstants[i])) m_openMouth.SetCurSel(i + 1);
			for (int i = 0; i < n; i++) if (el.value() == ("head_left_rotation" + facialConstants[i])) m_rotationLeft.SetCurSel(i + 1);
			for (int i = 0; i < n; i++) if (el.value() == ("head_right_rotation" + facialConstants[i])) m_rotationRight.SetCurSel(i + 1);
		}			
	}

	// Set config data
	globalShowFPS = general["view"]["show_fps"]; // FPS
	globalLowLight = general["view"]["low_light_indicator_on"]; // LIGHT
	globalSpeech = modules["speech"]["enabled"]; // SPEECH
	globalCameraNr = general["camera"]["camera_nr"]; // CAMERA
	globalMouseNose = events["nose_tracking"]["scaling_factor"] / 10;
	globalMouseEye = modules["eye"]["Eye_mouse_speed"];
	globalBoundBoxNose = events["nose_tracking"]["bound_sensitivity"];

	// FPS
	m_showFPS.SetWindowTextW(globalShowFPS ? L"ON" : L"OFF");
	// Low Light
	m_lowLightOn.SetWindowTextW(globalLowLight ? L"ON" : L"OFF");
	// Camera
	for (int i = 0; i < MAX_CAMERA_INDEX; i++)
	{
		CString curIndex;
		curIndex.Format(_T("Camera %d"), i+1);
		m_camera.AddString(curIndex);
	}
	m_camera.SetCurSel(globalCameraNr);
	// Just keep this here in case we want to use it?
	// strSliderValue.Format(_T("%d"), globalCameraNr);
	// m_cameraValue.SetWindowText(strSliderValue);
	CString strSliderValue;
	// Nose Mouse Speed
	m_noseMouseSpeed.SetRange(1, 100);
	m_noseMouseSpeed.SetPos(globalMouseNose);
	strSliderValue.Format(_T("%d"), globalMouseNose);
	m_noseMouseSpeedValue.SetWindowText(strSliderValue);
	// Eyes Mouse Speed
	m_eyesMouseSpeed.SetRange(1, 20);
	m_eyesMouseSpeed.SetPos(globalMouseEye);
	strSliderValue.Format(_T("%d"), globalMouseEye);
	m_eyesMouseSpeedValue.SetWindowText(strSliderValue);
	// NoseBox
	m_noseBoxBond.SetRange(1, 10);
	m_noseBoxBond.SetPos(globalBoundBoxNose);
	strSliderValue.Format(_T("%d"), globalBoundBoxNose);
	m_noseBoxBondValue.SetWindowText(strSliderValue);

	return TRUE;  // return TRUE  unless you set the focus to a control
}



// Save 
void CMFCUCLMI3SettingsDlg::Save(){
	// Update values
	if (m_modeNose.GetCheck() && m_methodFacial.GetCheck()) globalCurrentMode = GRID_NOSE_FACIAL;
	else if (m_modeEyes.GetCheck() && m_methodFacial.GetCheck()) globalCurrentMode = GRID_EYES_FACIAL;
	else if (m_modeNose.GetCheck() && m_methodSpeech.GetCheck()) globalCurrentMode = GRID_NOSE_SPEECH;
	else if (m_modeEyes.GetCheck() && m_methodSpeech.GetCheck()) globalCurrentMode = GRID_EYES_SPEECH;

	globalCameraNr = m_camera.GetCurSel();
	globalMouseNose = m_noseMouseSpeed.GetPos() * 10;
	globalMouseEye = m_eyesMouseSpeed.GetPos();

	globalMouseNose = m_noseMouseSpeed.GetPos() * 10;
	globalBoundBoxNose = m_noseBoxBond.GetPos();

	// --------------------- WRITE JSON ---------------------

	// Save Modes 
	/*
	wstring tempStrModes = L"data\\mode_controller.json";
	LPCWSTR pathModes = tempStrModes.c_str();
	ifstream ifs_modes(pathModes);
	string content_modes((istreambuf_iterator<char>(ifs_modes)), (istreambuf_iterator<char>()));
	json myjson_modes = json::parse(content_modes);
	myjson_modes["current_mode"] = globalCurrentMode;
	
	// Get data from current mode
	auto& modes = myjson_modes["modes"][globalCurrentMode];

	// Facial switches 
	json facialData = json::array();
	if (m_smile.GetCurSel() > 0) facialData.push_back("head_smile" + facialConstants[m_smile.GetCurSel() - 1]);
	if (m_fishFace.GetCurSel() > 0) facialData.push_back("head_fishface" + facialConstants[m_fishFace.GetCurSel() - 1]);
	if (m_raisedEyebrows.GetCurSel() > 0) facialData.push_back("head_raise_eyebrows" + facialConstants[m_raisedEyebrows.GetCurSel() - 1]);
	if (m_openMouth.GetCurSel() > 0) facialData.push_back("head_open_mouth" + facialConstants[m_openMouth.GetCurSel() - 1]);
	if (m_rotationLeft.GetCurSel() > 0) facialData.push_back("head_left_rotation" + facialConstants[m_rotationLeft.GetCurSel() - 1]);
	if (m_rotationRight.GetCurSel() > 0) facialData.push_back("head_right_rotation" + facialConstants[m_rotationRight.GetCurSel() - 1]);

	for (auto& el : modes.items()) {
		string cur = el.value();
		if(
			cur.find("head_smile") == string::npos &&
			cur.find("head_fishface") == string::npos &&
			cur.find("head_raise_eyebrows") == string::npos &&
			cur.find("head_open_mouth") == string::npos &&
			cur.find("head_left_rotation") == string::npos &&
			cur.find("head_right_rotation") == string::npos 
		) facialData.push_back(cur.c_str());
	}

	modes = facialData;

	ofstream outputModesFile(pathModes);
	outputModesFile << setw(4) << myjson_modes << endl;
	*/
	// Save Configs
	
	wstring tempStrConfig = L"data\\configMFC.json";
	//wstring tempStrConfig = L"main.dist\\settings\\test_settings_MFC.json";
	LPCWSTR pathConfig = tempStrConfig.c_str();
	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));
	json myjson_config = json::parse(content_config);
	auto& general = myjson_config["general"];
	auto& modules = myjson_config["modules"];
	auto& events = myjson_config["events"];
	modules["speech"]["enabled"] = globalSpeech;
	general["view"]["show_fps"] = globalShowFPS;
	general["view"]["low_light_indicator_on"] = globalLowLight;
	general["camera"]["camera_nr"] = globalCameraNr; 
	events["nose_tracking"]["scaling_factor"] = globalMouseNose;
	modules["eye"]["Eye_mouse_speed"] = globalMouseEye;
	events["nose_tracking"]["bound_sensitivity"] = globalBoundBoxNose;
	

	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFile(pathConfig);
	outputConfigFile << setw(4) << myjson_config << endl;

	//MessageBox(_T("UCL MotionInput will now restart and apply the new setting."), _T("Information"));
    //MessageBox(_T("Any changes made have now been saved.\n\nMotionInput will now be restarted to apply the new settings."), _T("Changes Saved"));

	// 1. Exit MI
	//system("TASKKILL /IM MI3-FacialNavigation-3.11.exe");

	// 2. Copy amended configMFC.json file from MFC app to config.json
	Sleep(100);	// 1 seconds delay
	ifstream src(L"data\\configMFC.json", ios::binary);
	ofstream dst(L"data\\config.json", ios::binary);
	dst << src.rdbuf();

	// 3. Run Illumiroom
	ShellExecuteA(NULL, "open", "main.dist\\main.exe", NULL, NULL, SW_SHOWDEFAULT);

	//Add option on dialog to keep window open, or close automatically
	//CDialogEx::OnOK();
}

// About
void CMFCUCLMI3SettingsDlg::ShowAbout()
{
	m_aboutDlg.DoModal();
}

// Show Help
void CMFCUCLMI3SettingsDlg::ShowHelp()
{
	// OPEN help.txt
	CComHeapPtr<WCHAR> pszPath;
	if (SHGetKnownFolderPath(FOLDERID_Windows, KF_FLAG_CREATE, nullptr, &pszPath) == S_OK)
	{
		// relative path
		wstring tempStr = L"data\\help\\head\\help.txt";
		LPCWSTR finalP = tempStr.c_str();

		// open .txt file
		SHELLEXECUTEINFO si = { sizeof(SHELLEXECUTEINFO) };
		si.hwnd = GetSafeHwnd();
		si.lpVerb = L"open";
		si.lpFile = finalP;
		si.nShow = SW_SHOW;
		ShellExecuteEx(&si);
	}
}


void CMFCUCLMI3SettingsDlg::OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar){
	CSliderCtrl* pSlider = reinterpret_cast<CSliderCtrl*>(pScrollBar);

	// Nose Mouse Speed
	if (pSlider == &m_noseMouseSpeed) {
		CString strSliderValue;
		int iValue = m_noseMouseSpeed.GetPos(); // Get Slider value
		strSliderValue.Format(_T("%d"), iValue);
		m_noseMouseSpeedValue.SetWindowText(strSliderValue);
	}// Eyes Mouse Speed
	else if (pSlider == &m_eyesMouseSpeed) {
		CString strSliderValue;
		int iValue = m_eyesMouseSpeed.GetPos(); // Get Slider value
		strSliderValue.Format(_T("%d"), iValue);
		m_eyesMouseSpeedValue.SetWindowText(strSliderValue);
	}// NoseBox Bound
	else if (pSlider == &m_noseBoxBond) {
		CString strSliderValue;
		int iValue = m_noseBoxBond.GetPos(); // Get Slider value
		strSliderValue.Format(_T("%d"), iValue);
		m_noseBoxBondValue.SetWindowText(strSliderValue);
	}
}

// FPS 
void CMFCUCLMI3SettingsDlg::UpdateShowFPS(){
	CString temp2;
	m_showFPS.GetWindowText(temp2);
	if (temp2 == "ON"){
		m_showFPS.SetWindowText(L"OFF");
		globalShowFPS = false;
	}
	else {
		m_showFPS.SetWindowTextW(L"ON");
		globalShowFPS = true;
	}
}

// Low Light
void CMFCUCLMI3SettingsDlg::UpdateLowLight(){
	CString temp2;
	m_lowLightOn.GetWindowText(temp2);
	if (temp2 == "ON") {
		m_lowLightOn.SetWindowText(L"OFF");
		globalLowLight = false;
	}
	else {
		m_lowLightOn.SetWindowTextW(L"ON");
		globalLowLight = true;
	}
}
// Do not show on/off eye gaze option if Nose Facial selected
void CMFCUCLMI3SettingsDlg::UpdateModeNose(){
	m_modeNose.SetCheck(1);
	m_modeEyes.SetCheck(0);

	reference_wrapper<CComboBox> boxes[] = { m_smile, m_fishFace, m_raisedEyebrows, m_openMouth, m_rotationLeft, m_rotationRight };
	string titles[] = { "head_smile", "head_fishface", "head_raise_eyebrows", "head_open_mouth", "head_left_rotation", "head_right_rotation" };
	for (CComboBox& box : boxes) for (int i = box.GetCount() - 1; i > 0; i--) box.DeleteString(i);

	int n = m_methodFacial.GetCheck() ? 5 : 0;
	for (CComboBox& box : boxes) for (int i = 0; i < n; i++) box.AddString(facialValues[i]);


	auto& modes = globalModesData[GRID_NOSE_FACIAL];
	for (auto& el : modes.items()) for (int t = 0; t < 6; t++) for (int i = 0; i < n; i++)
		if (el.value() == (titles[t] + facialConstants[i])) boxes[t].get().SetCurSel(i + 1);
}

// Show all options on Eyes Facial
void CMFCUCLMI3SettingsDlg::UpdateModeEyes(){
	m_modeNose.SetCheck(0);
	m_modeEyes.SetCheck(1);

	reference_wrapper<CComboBox> boxes[] = { m_smile, m_fishFace, m_raisedEyebrows, m_openMouth, m_rotationLeft, m_rotationRight };
	string titles[] = { "head_smile", "head_fishface", "head_raise_eyebrows", "head_open_mouth", "head_left_rotation", "head_right_rotation"};
	for (CComboBox& box : boxes) for (int i = box.GetCount() - 1; i > 0; i--) box.DeleteString(i);

	auto& modes = globalModesData[GRID_EYES_FACIAL];
	int n = m_methodFacial.GetCheck() ? 6 : 0;
	for (CComboBox& box : boxes) for (int i = 0; i < n; i++) box.AddString(facialValues[i]);
	for (auto& el : modes.items()) for (int t = 0; t < 6; t++) for (int i = 0; i < n; i++) 
		if (el.value() == (titles[t] + facialConstants[i])) boxes[t].get().SetCurSel(i + 1);
}

// Show options only when Facial selected
void CMFCUCLMI3SettingsDlg::UpdateMethodFacial(){
	m_methodFacial.SetCheck(1);
	m_methodSpeech.SetCheck(0);

	reference_wrapper<CComboBox> boxes[] = { m_smile, m_fishFace, m_raisedEyebrows, m_openMouth, m_rotationLeft, m_rotationRight };
	string titles[] = { "head_smile", "head_fishface", "head_raise_eyebrows", "head_open_mouth", "head_left_rotation", "head_right_rotation" };
	for (CComboBox& box : boxes) for (int i = box.GetCount() - 1; i > 0; i--) box.DeleteString(i);

	auto& modes = globalModesData[m_modeEyes.GetCheck() ? GRID_EYES_FACIAL : GRID_NOSE_FACIAL];
	int n = m_modeEyes.GetCheck() ? 6 : 5;
	for (CComboBox& box : boxes) for (int i = 0; i < n; i++) box.AddString(facialValues[i]);
	for (auto& el : modes.items()) for (int t = 0; t < 6; t++) for (int i = 0; i < n; i++)
		if (el.value() == (titles[t] + facialConstants[i])) boxes[t].get().SetCurSel(i + 1);
}
void CMFCUCLMI3SettingsDlg::UpdateMethodSpeech(){
	m_methodFacial.SetCheck(0);
	m_methodSpeech.SetCheck(1);

	reference_wrapper<CComboBox> boxes[] = { m_smile, m_fishFace, m_raisedEyebrows, m_openMouth, m_rotationLeft, m_rotationRight };
	
	for (CComboBox& box : boxes) {
		for (int i = box.GetCount() - 1; i > 0; i--) box.DeleteString(i);
		box.SetCurSel(0);
	}
}



// Popups
void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMode()
{
    MessageBox(_T("The Tracking Mode selected is used to control the device through either Nose or Eyes tracking. \nWhile using Eyes Mode the cursor of the mouse follows a person's eye gaze and moves across the screen. \nNose Mode requires some neck mobility as it is needed when pointing nose up, down, left, and right."), _T("Tracking Mode Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMethod()
{
    MessageBox(_T("The choice of using Speech or Facial methods to carry out actionsis available no matter the Tracking Mode selected. For instance, consider a left mouse click and a right mouse click. These actions could be triggered via Speech Commands with saying 'click' and 'right click' or via Facial Switches. \n\nWith Speech Commands, a person controls computer actions by saying specific phrases linked to actions. Currently, Speech Commands are designed to be used by people who are able to pronounce common words clearly. \n\nThere are six Facial Switches/Movements recognised by MotionInput at the moment. When Facial Method is selected the Facial Mode section is activated and a computer action becomes available to select for each movement."), _T("Method Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFps()
{
	MessageBox(_T("FPS, or Frames per second, is the rate of frames (pictures) produced every second. The higher the number is, the smoother and better the interaction with the device will be. \n\nBy default, this setting is set to 'ON' meaning the FPS number shows at the bottom right corner of MotionInput's camera screen. Changing this option to 'OFF' will hide the FPS number."), _T("FPS Information"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoLight()
{
    MessageBox(_T("Using MotionInput in a place with low lighting can cause visual control commands to not be recognised accordingly.In this case, setting Low Light option 'ON' is likely to improve interaction with MotionInput.\n\nThe Low Light indicator is set to'OFF' by default."), _T("Low Light Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCamera()
{
    MessageBox(_T("Some computer devices may have two or more webcams available for MotionInput to use (such as Microsoft Surface devices which often have a front and a rear camera). Some users might also prefer attaching an additional camera(s) to their computer devices. \n\nThe default camera value is initially set to 0. If you are experiencing difficulties with MotionInput camera detection, set this option to a different number. In most cases, changing 0 to 1 or 2 is likely to be a solution. \nRestart MotionInput to check if the new number selected has resolved the problem. If not adjust the setting again until MotionInput is connected to the desired camera."), _T("Default Camera Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoNoseMouse()
{
    MessageBox(_T("This option allows users to adjust the speed with which the mouse moves across the screen using Nose Mode. The lower the number the slower the mouse will move and vice versa."), _T("Nose Mode Speed Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoNoseboxBound()
{
    MessageBox(_T("Distance is only used during Nose Mode with Speech Method. A lower number allows setting the box size (range)wit more ease. Distance ranges allow users to specify the trajectory of the movement to be made before triggering a bound setup."), _T("Nose Mode Distance Information"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoEyesMouse()
{
    MessageBox(_T("This option allows specification of the speed with which the mouse moves across the screen using Eyes Mode. The lower the number the slower the mouse will move and vice versa."), _T("Eyes Mouse Speed Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSmile()
{
    MessageBox(_T("To trigger the Smile Facial gesture try to make part of your teeth visible, try saying 'cheese'."), _T("Smile Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFishface()
{
    MessageBox(_T("Fish Face is a gesture where a person's lips come together in a small circle in the middle of their face. Similar facial movement to that gestures made during a peck kiss or  whistling."), _T("Fish Face Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoEyebrows()
{
    MessageBox(_T("Eyebrows raise can be seen when making a surprised or scared facial expression. It can also happen if a person looks up in attempt to see their forehead without the use of a mirror. \nIf experiencing difficulty triggering this gesture, try lowering your eyebrows (making a grumpy face) and then raising them again."), _T("Raised Eyebrows Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoOpenMouth()
{
    MessageBox(_T("An Open Mouth gesture should be a relaxed movement as, typically, a standard circleforms during this process."), _T("Open Mouth Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoRotateHeadLeft()
{
    MessageBox(_T("This movement resembles the movement puppies (dogs) make when looking at an object/individual with great curiousity. The head tilts to the side while keeping the nose in its original position.\n\nTry moving your head towards your left sholder."), _T("Rotate Head Left Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoRotateHeadRight()
{
    MessageBox(_T("This movement resembles the movement puppies (dogs) make when looking at an object/individual with great curiousity. The head tilts to the side while keeping the nose in its original position.\n\nTry moving your head towards your right sholder."), _T("Rotate Head Right Information"));
}




void CMFCUCLMI3SettingsDlg::OnCbnSelchangeDefaultcameraCombo()
{
	// TODO: Add your control notification handler code here
}


void CMFCUCLMI3SettingsDlg::OnBnClickedCancel()
{
	// TODO: Add your control notification handler code here
	CDialogEx::OnCancel();
}
