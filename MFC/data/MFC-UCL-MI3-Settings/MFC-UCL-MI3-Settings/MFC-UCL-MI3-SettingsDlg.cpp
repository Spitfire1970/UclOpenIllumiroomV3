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

int globalCameraNr;
bool globalShowFPS;
bool globalLowLight;
int globalMouseEye;



// parameters
#define MAX_CAMERA_INDEX 9





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
	//DDX_Control(pDX, IDC_NOSESPEED_SLIDER, m_noseMouseSpeed);
	//DDX_Control(pDX, IDC_EDIT3, m_cameraValue);
	//DDX_Control(pDX, IDC_NOSESPEED_COUNTER, m_noseMouseSpeedValue);
	DDX_Control(pDX, IDC_EYEMOUSE_SPEED_SLIDER, m_eyesMouseSpeed);
	DDX_Control(pDX, IDC_EYEMOUSE_SPEED_COUNTER, m_eyesMouseSpeedValue);
	DDX_Control(pDX, IDC_FPS_BUTTON, m_showFPS);
	DDX_Control(pDX, IDC_LOW_LIGHT_BUTTON, m_lowLightOn);
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
	ON_BN_CLICKED(IDC_BUTTON_INFO_FPS, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFps)
	ON_BN_CLICKED(IDC_BUTTON_INFO_LIGHT, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoLight)
	ON_BN_CLICKED(IDC_BUTTON_INFO_CAMERA, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCamera)

	ON_CBN_SELCHANGE(IDC_DEFAULTCAMERA_COMBO, &CMFCUCLMI3SettingsDlg::OnCbnSelchangeDefaultcameraCombo)
	ON_BN_CLICKED(IDCANCEL, &CMFCUCLMI3SettingsDlg::OnBnClickedCancel)
	ON_BN_CLICKED(IDSAVEONLY, &CMFCUCLMI3SettingsDlg::OnBnClickedSaveonly)
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
	wstring pathConfigS = L"main.dist\\settings\\general_settings.json";
	LPCWSTR pathConfig = pathConfigS.c_str();


	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));

	json general_settings = json::parse(content_config);
	//auto& general = myjson_config["general"];
	//auto& modules = myjson_config["modules"];

	


	// Set config data
	globalShowFPS = general_settings["show_fps"]; // FPS
	globalLowLight = general_settings["view"]["low_light_indicator_on"]; // LIGHT
	globalCameraNr = general_settings["camera"]["camera_nr"]; // CAMERA
	//globalMouseNose = events["nose_tracking"]["scaling_factor"] / 10;
	globalMouseEye = general_settings["eye"]["Eye_mouse_speed"];
	//globalBoundBoxNose = events["nose_tracking"]["bound_sensitivity"];

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
	//m_noseMouseSpeed.SetRange(1, 100);
	//m_noseMouseSpeed.SetPos(globalMouseNose);
	//strSliderValue.Format(_T("%d"), globalMouseNose);
	//m_noseMouseSpeedValue.SetWindowText(strSliderValue);
	// Eyes Mouse Speed
	m_eyesMouseSpeed.SetRange(1, 20);
	m_eyesMouseSpeed.SetPos(globalMouseEye);
	strSliderValue.Format(_T("%d"), globalMouseEye);
	m_eyesMouseSpeedValue.SetWindowText(strSliderValue);
	// NoseBox
	//m_noseBoxBond.SetRange(1, 10);
	//m_noseBoxBond.SetPos(globalBoundBoxNose);
	//strSliderValue.Format(_T("%d"), globalBoundBoxNose);
	//m_noseBoxBondValue.SetWindowText(strSliderValue);

	return TRUE;  // return TRUE  unless you set the focus to a control
}



// Save 
void CMFCUCLMI3SettingsDlg::Save(){
	// Update values

	globalCameraNr = m_camera.GetCurSel();

	globalMouseEye = m_eyesMouseSpeed.GetPos();

	
	wstring tempStrConfig = L"main.dist\\settings\\general_settings.json";
	LPCWSTR pathConfig = tempStrConfig.c_str();
	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));
	json general_settings = json::parse(content_config);

	general_settings["show_fps"] = globalShowFPS;
	general_settings["view"]["low_light_indicator_on"] = globalLowLight;
	general_settings["camera"]["camera_nr"] = globalCameraNr;
	general_settings["eye"]["Eye_mouse_speed"] = globalMouseEye;
	

	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFile(pathConfig);
	outputConfigFile << setw(4) << general_settings << endl;

	//MessageBox(_T("UCL MotionInput will now restart and apply the new setting."), _T("Information"));
    //MessageBox(_T("Any changes made have now been saved.\n\nMotionInput will now be restarted to apply the new settings."), _T("Changes Saved"));

	// 1. Exit MI
	//system("TASKKILL /IM MI3-FacialNavigation-3.11.exe");

	// 2. Copy amended configMFC.json file from MFC app to config.json
	Sleep(100);	// 1 seconds delay
	
	/*
	ifstream src(L"main.dist\\settings\\temp_settings.json", ios::binary);
	ofstream dst(L"main.dist\\settings\\general_settings.json", ios::binary);
	dst << src.rdbuf();*/

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

	// eyes Mouse Speed

	if (pSlider == &m_eyesMouseSpeed) {
		CString strSliderValue;
		int iValue = m_eyesMouseSpeed.GetPos(); // Get Slider value
		strSliderValue.Format(_T("%d"), iValue);
		m_eyesMouseSpeedValue.SetWindowText(strSliderValue);
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





void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoEyesMouse()
{
    MessageBox(_T("This option allows specification of the speed with which the mouse moves across the screen using Eyes Mode. The lower the number the slower the mouse will move and vice versa."), _T("Eyes Mouse Speed Information"));
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




void CMFCUCLMI3SettingsDlg::OnBnClickedSaveonly()
{
	// Update values

	globalCameraNr = m_camera.GetCurSel();

	globalMouseEye = m_eyesMouseSpeed.GetPos();


	wstring tempStrConfig = L"main.dist\\settings\\temp_settings.json";
	LPCWSTR pathConfig = tempStrConfig.c_str();
	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));
	json general_settings = json::parse(content_config);

	general_settings["show_fps"] = globalShowFPS;
	general_settings["view"]["low_light_indicator_on"] = globalLowLight;
	general_settings["camera"]["camera_nr"] = globalCameraNr;
	general_settings["eye"]["Eye_mouse_speed"] = globalMouseEye;


	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFile(pathConfig);
	outputConfigFile << setw(4) << general_settings << endl;

	//MessageBox(_T("UCL MotionInput will now restart and apply the new setting."), _T("Information"));
	//MessageBox(_T("Any changes made have now been saved.\n\nMotionInput will now be restarted to apply the new settings."), _T("Changes Saved"));

	// 1. Exit MI
	//system("TASKKILL /IM MI3-FacialNavigation-3.11.exe");

	// 2. Copy amended configMFC.json file from MFC app to config.json
	Sleep(100);	// 1 seconds delay

	ifstream src(L"main.dist\\settings\\temp_settings.json", ios::binary);
	ofstream dst(L"main.dist\\settings\\general_settings.json", ios::binary);
	dst << src.rdbuf();
}
