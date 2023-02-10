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

// parameters
#define MAX_CAMERA_INDEX 10

// define json library
using json = nlohmann::json;
using namespace std;

// define global variables
string globalCurrentMode;
bool globalSpeech;
int globalCameraNr;
double globalPinch;
bool globalShowFPS;
bool globalLowLight;

// Define grids
#define MODE_RIGHT_TOUCH "touchpoints_right_hand_speech"
#define MODE_RIGHT_BASIC "basic_right_hand_speech"
#define MODE_LEFT_TOUCH "touchpoints_left_hand_speech"
#define MODE_LEFT_BASIC "basic_left_hand_speech"

// CMFCUCLMI3SettingsDlg Dialog - MFC VARIABLES
CMFCUCLMI3SettingsDlg::CMFCUCLMI3SettingsDlg(CWnd* pParent) : CDialogEx(IDD_MFCUCLMI3SETTINGS_DIALOG, pParent){
	//UCL LOGO ICON
	m_hIcon = AfxGetApp()->LoadIcon(IDI_ICON1);
	// uncomment below for the MFC default logo (and comment the line above)
	//m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CMFCUCLMI3SettingsDlg::DoDataExchange(CDataExchange* pDX){
	CDialogEx::DoDataExchange(pDX);

	
	DDX_Control(pDX, IDC_FPS_BUTTON, m_showFPS);
	DDX_Control(pDX, IDC_DEFAULT_CAMERA_COMBO, m_camera);
	
	
	DDX_Control(pDX, IDC_LOW_LIGHT_BUTTON, m_lowLightOn);
	DDX_Control(pDX, IDC_TOUCH_POINTS_BUTTON, m_modeTouch);
	DDX_Control(pDX, IDC_NORMAL_MOUSE_BUTTON, m_modeClassic);
	DDX_Control(pDX, IDC_HAND_LEFT_BUTTON, m_handLeft);
	DDX_Control(pDX, IDC_HAND_RIGHT_BUTTON, m_handRight);
	DDX_Control(pDX, IDC_PINCH_SLIDER, m_pinchSpeed);
	DDX_Control(pDX, IDC_SPEECH_ACTIVE_BUTTON, m_speech);
	DDX_Control(pDX, IDC_PINCH_COUNTER, m_pinchSpeedValue);
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
	ON_BN_CLICKED(IDC_TOUCH_POINTS_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateModeTouch)
	ON_BN_CLICKED(IDC_NORMAL_MOUSE_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateModeClassic)
	ON_BN_CLICKED(IDC_HAND_LEFT_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateHandLeft)
	ON_BN_CLICKED(IDC_HAND_RIGHT_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateHandRight)
    ON_BN_CLICKED(IDC_BUTTON_INFO_MODE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMode)
    ON_BN_CLICKED(IDC_BUTTON_INFO_PREFERENCE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMethod)
    ON_BN_CLICKED(IDC_BUTTON_INFO_FPS, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFps)
    ON_BN_CLICKED(IDC_BUTTON_INFO_LIGHT, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoLight)
    ON_BN_CLICKED(IDC_BUTTON_INFO_DEFAULT_CAMERA, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCamera)
	ON_BN_CLICKED(IDC_BUTTON_INFO_PINCH, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoPinch)
	ON_BN_CLICKED(IDC_BUTTON_INFO_ACTIVE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSpeech)
	ON_BN_CLICKED(IDC_SPEECH_ACTIVE_BUTTON, &CMFCUCLMI3SettingsDlg::UpdateSpeech)
	
	ON_STN_CLICKED(IDC_STATIC_DEFAULT_CAMERA, &CMFCUCLMI3SettingsDlg::OnStnClickedStaticDefaultCamera)
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
	m_modeTouch.SetCheck(current_mode == MODE_LEFT_TOUCH || current_mode == MODE_RIGHT_TOUCH);
	m_modeClassic.SetCheck(current_mode == MODE_LEFT_BASIC || current_mode == MODE_RIGHT_BASIC);
	m_handLeft.SetCheck(current_mode == MODE_LEFT_TOUCH || current_mode == MODE_LEFT_BASIC);
	m_handRight.SetCheck(current_mode == MODE_RIGHT_TOUCH || current_mode == MODE_RIGHT_BASIC);

	// Set config data
	globalShowFPS = general["view"]["show_fps"]; // FPS
	globalLowLight = general["view"]["low_light_indicator_on"]; // LIGHT
	globalSpeech = modules["speech"]["enabled"]; // SPEECH
	globalCameraNr = general["camera"]["camera_nr"]; // CAMERA
	globalPinch = ((double) modules["hand"]["position_pinch_sensitivity"]) * 100;

	// FPS
	m_showFPS.SetWindowTextW(globalShowFPS ? L"ON" : L"OFF");
	// Low Light
	m_lowLightOn.SetWindowTextW(globalLowLight ? L"ON" : L"OFF");
	m_speech.SetWindowTextW(globalSpeech ? L"ON" : L"OFF");
	// Camera
	// Camera Index (0 to MAX_CAMERA_INDEX)
	for (int i = 0; i < MAX_CAMERA_INDEX; i++)
	{
		CString curIndex;
		curIndex.Format(_T("Camera %d"), i);
		m_camera.AddString(curIndex);
	}
	m_camera.SetCurSel(globalCameraNr);
	// Nose Mouse Speed
	m_pinchSpeed.SetRange(1, 100);
	m_pinchSpeed.SetPos(globalPinch);
	CString strSliderValue;
	strSliderValue.Format(_T("%d"), int(globalPinch));
	m_pinchSpeedValue.SetWindowText(strSliderValue);

	return TRUE;  // return TRUE  unless you set the focus to a control
}



// Save 
void CMFCUCLMI3SettingsDlg::Save(){
	// Update values
	if (m_modeTouch.GetCheck() && m_handLeft.GetCheck()) globalCurrentMode = MODE_LEFT_TOUCH;
	else if (m_modeClassic.GetCheck() && m_handLeft.GetCheck()) globalCurrentMode = MODE_LEFT_BASIC;
	else if (m_modeTouch.GetCheck() && m_handRight.GetCheck()) globalCurrentMode = MODE_RIGHT_TOUCH;
	else if (m_modeClassic.GetCheck() && m_handRight.GetCheck()) globalCurrentMode = MODE_RIGHT_BASIC;

	globalCameraNr = m_camera.GetCurSel();
	globalPinch = ((double) m_pinchSpeed.GetPos()) / 100.;

	// --------------------- WRITE JSON ---------------------

	// Save Modes
	wstring tempStrModes = L"data\\mode_controller.json";
	LPCWSTR pathModes = tempStrModes.c_str();
	ifstream ifs_modes(pathModes);
	string content_modes((istreambuf_iterator<char>(ifs_modes)), (istreambuf_iterator<char>()));
	json myjson_modes = json::parse(content_modes);
	myjson_modes["current_mode"] = globalCurrentMode;
	
	ofstream outputModesFile(pathModes);
	outputModesFile << setw(4) << myjson_modes << endl;

	// Save Configs
	wstring tempStrConfig = L"data\\configMFC.json";
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
	modules["hand"]["position_pinch_sensitivity"] = globalPinch;
	

	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFile(pathConfig);
	outputConfigFile << setw(4) << myjson_config << endl;

	//MessageBox(_T("UCL MotionInput will now restart and apply the new setting."), _T("Information"));
	MessageBox(_T("Any changes made have now been saved.\n\nUCL Open-Illumiroom V2 will now be restarted to apply the new settings."), _T("Changes Saved"));

	// 1. Exit MI
	//system("TASKKILL /IM MI3-Multitouch-3.11.exe");

	// 2. Copy amended configMFC.json file from MFC app to config.json
	Sleep(100);	// 1 seconds delay
	ifstream src(L"data\\configMFC.json", ios::binary);
	ofstream dst(L"data\\config.json", ios::binary);
	dst << src.rdbuf();


	// 3. Run Illumiroom
	ShellExecuteA(NULL, "open", "main.dist\\main.exe", NULL, NULL, SW_SHOWDEFAULT);


	CDialogEx::OnOK();
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
		wstring tempStr = L"data\\help\\hand\\help.txt";
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

        // Camera
    if (pSlider == &m_pinchSpeed) {
		CString strSliderValue;
		int iValue = m_pinchSpeed.GetPos(); // Get Slider value
		strSliderValue.Format(_T("%d"), iValue);
		m_pinchSpeedValue.SetWindowText(strSliderValue);
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
void CMFCUCLMI3SettingsDlg::UpdateModeTouch(){
	m_modeTouch.SetCheck(1);
	m_modeClassic.SetCheck(0);
}

// Show all options on Eyes Facial
void CMFCUCLMI3SettingsDlg::UpdateModeClassic(){
	m_modeTouch.SetCheck(0);
	m_modeClassic.SetCheck(1);
}

// Show options only when Facial selected
void CMFCUCLMI3SettingsDlg::UpdateHandLeft(){
	m_handLeft.SetCheck(1);
	m_handRight.SetCheck(0);
}
void CMFCUCLMI3SettingsDlg::UpdateHandRight(){
	m_handLeft.SetCheck(0);
	m_handRight.SetCheck(1);
}


void CMFCUCLMI3SettingsDlg::UpdateSpeech(){
	CString temp2;
	m_speech.GetWindowText(temp2);
	if (temp2 == "ON") {
		m_speech.SetWindowText(L"OFF");
		globalSpeech = false;
	}
	else {
		m_speech.SetWindowTextW(L"ON");
		globalSpeech = true;
	}
}


// Popups
void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMode(){
	MessageBox(_T("'Touch Points' allows users to interact with a computer device using gestures to trigger a response similar to that of a touch screen on a tablet. On some devices Touch Points might be better suited for actions such as scrolling, zooming, and dragging.\n'Normal Mouse' triggers events which mimic computer mouse actions."), _T("In-Air Pointer Type Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoMethod(){
	MessageBox(_T("Selecting 'Left' or 'Right' indicates the dominant hand which will be used to move the mouse across the screen.\nAll other hand gestures are done using the right hand."), _T("Hand Preference Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFps(){
    MessageBox(_T("FPS, or Frames per second, is the rate of frames (pictures) produced every second. The higher the number is, the smoother and better the interaction with the device will be. \n\nBy default, this setting is set to 'ON' meaning the FPS number shows at the bottom right corner of MotionInput's camera screen. Changing this option to 'OFF' will hide the FPS number."), _T("FPS Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoLight(){
	MessageBox(_T("Using MotionInput in a place with low lighting can cause visual control commands to not be recognised accordingly.In this case, setting Low Light option 'ON' is likely to improve interaction with MotionInput.\n\nThe Low Light indicator is set to'OFF' by default."), _T("Low Light Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCamera(){
	MessageBox(_T("Some computer devices may have two or more webcams available for MotionInput to use (such as Microsoft Surface devices which often have a front and a rear camera). Some users might also prefer attaching an additional camera(s) to their computer devices. \n\nThe default camera value is initially set to 0. If you are experiencing difficulties with MotionInput camera detection, set this option to a different number. In most cases, changing 0 to 1 or 2 is likely to be a solution. \nRestart MotionInput to check if the new number selected has resolved the problem. If not adjust the setting again until MotionInput is connected to the desired camera."), _T("Default Camera Information"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoPinch(){
	MessageBox(_T("The most commonly used hand gesture in Multitouch is a 'Pinch' where the thumb and the index finger touch to make a shape similar to an elipse. \nThis option allows the user to adjust the sensitivity with which this gesture is recognised. If you find that a pinch hand gesture is to easily recognised or too difficult to trigger, raise or lower the value accordingly."), _T("Pinch Sensitivity Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSpeech(){
	MessageBox(_T("Speech can be enabled no matter the In-Air Pointer or Hand Preference selected. \nSpeech commands allow users to trigger various computer actions without any physical movement.  \n\nUsers can use Speech to control various computer actions by saying key phrases. \nFor instance, saying 'click' triggers a left mouse click and saying 'double click' triggers a double left mouse click.Speech 'ON' allows for more functionality than Touch Points or Normal Mouse pointers alone. \n\nCurrently, Speech Commands are designed to be used by people who are able to pronounce common words clearly."), _T("Speech Information"));
}







void CMFCUCLMI3SettingsDlg::OnStnClickedStaticDefaultCamera()
{
	// TODO: Add your control notification handler code here
}
