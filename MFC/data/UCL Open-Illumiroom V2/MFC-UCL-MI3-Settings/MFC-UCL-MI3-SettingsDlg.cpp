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

//general settings
int globalCameraNr;
bool globalShowFPS;
bool globalSettingsDialogOpen;
bool globalUseCalibration;

//mode settings
int globalBlurAmount;
string globalSelectedSnowAmount;
string globalSelectedRainAmount;

string globalSelectedMode;
int globalSelectedModeNum = 0;

string modesAvailableStr[] = { "blur","wobble","cartoon","weather","snow","rain","low_health","speed_blur","display_image"};
LPCWSTR  modesAvailable[] = { L"blur",L"wobble",L"cartoon",L"weather",L"snow",L"rain",L"low_health",L"speed_blur",L"display_image"};

LPCSTR runProgramPath = "UCL_Open-Illumiroom_V2.dist\\UCL_Open-Illumiroom_V2.exe";

LPCWSTR aboutSite = L"https://fabianbindley.github.io/IllumiroomGroup33COMP0016/";
// general settings config data
wstring pathConfigSGeneral = L"UCL_Open-Illumiroom_V2.dist\\settings\\general_settings.json";
// mode settings config data
wstring pathConfigSModes = L"UCL_Open-Illumiroom_V2.dist\\settings\\mode_settings.json";

// parameters
//MFC does not easily support calculating actual number of connected cameras
#define MAX_CAMERA_INDEX 5





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

	DDX_Control(pDX, IDC_BLUR_AMOUNT_SLIDER, m_blurAmount);
	DDX_Control(pDX, IDC_BLUR_AMOUNT_COUNTER, m_blurAmountValue);
	DDX_Control(pDX, IDC_FPS_BUTTON, m_showFPS);
	DDX_Control(pDX, IDC_SELECT_MODE_COMBO, m_selectMode);
	DDX_Control(pDX, IDC_KEEP_SETTINGS_OPEN, m_keepSettingsOpen);
	DDX_Control(pDX, IDC_USE_CALIBRATION, m_useCalibration);

	DDX_Control(pDX, IDC_SNOW1, m_lightSnow);
	DDX_Control(pDX, IDC_SNOW2, m_mediumSnow);
	DDX_Control(pDX, IDC_SNOW3, m_harshSnow);
	DDX_Control(pDX, IDC_RAIN1, m_drizzleRain);
	DDX_Control(pDX, IDC_RAIN2, m_heavyRain);
	DDX_Control(pDX, IDC_RAIN3, m_torrentialRain);

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
	ON_BN_CLICKED(IDC_BUTTON_INFO_FPS, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFps)
	ON_BN_CLICKED(IDC_BUTTON_INFO_CAMERA, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCamera)

	ON_CBN_SELCHANGE(IDC_DEFAULTCAMERA_COMBO, &CMFCUCLMI3SettingsDlg::OnCbnSelchangeDefaultcameraCombo)
	ON_BN_CLICKED(IDCANCEL, &CMFCUCLMI3SettingsDlg::OnBnClickedCancel)
	ON_BN_CLICKED(IDSAVEONLY, &CMFCUCLMI3SettingsDlg::OnBnClickedSaveonly)
	ON_BN_CLICKED(IDC_BUTTON_INFO_SNOW_MODE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSnowMode)
	ON_BN_CLICKED(IDC_BUTTON_INFO_BLUR_AMOUNT, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoBlurAmount)
	ON_BN_CLICKED(IDC_SELECT_DISPLAYS_BUTTON, &CMFCUCLMI3SettingsDlg::OnBnClickedSelectDisplaysButton)
	ON_BN_CLICKED(IDC_CALIBRATE_SYSTEM_BUTTON, &CMFCUCLMI3SettingsDlg::OnBnClickedCalibrateSystemButton)
	ON_BN_CLICKED(IDC_BUTTON_INFO_CALIBRATE_SYSTEM, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCalibrateSystem)


	ON_BN_CLICKED(IDCLOSEPROJECTOR, &CMFCUCLMI3SettingsDlg::OnBnClickedCloseprojector)
	ON_BN_CLICKED(IDC_STATIC_CAMERA_OPTIONS, &CMFCUCLMI3SettingsDlg::OnBnClickedStaticCameraOptions)
	ON_CBN_SELCHANGE(IDC_SELECT_MODE_COMBO, &CMFCUCLMI3SettingsDlg::OnCbnSelchangeSelectModeCombo)
	ON_BN_CLICKED(IDC_BUTTON_INFO_SELECT_MODE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSelectMode)
	ON_STN_CLICKED(IDC_STATIC_SELECT_MODE, &CMFCUCLMI3SettingsDlg::OnStnClickedStaticSelectMode)

	ON_BN_CLICKED(IDC_SNOW1, &CMFCUCLMI3SettingsDlg::OnBnClickedSnow1)
	ON_BN_CLICKED(IDC_SNOW2, &CMFCUCLMI3SettingsDlg::OnBnClickedSnow2)
	ON_BN_CLICKED(IDC_SNOW3, &CMFCUCLMI3SettingsDlg::OnBnClickedSnow3)
	ON_BN_CLICKED(IDC_KEEP_SETTINGS_OPEN, &CMFCUCLMI3SettingsDlg::OnBnClickedKeepSettingsOpen)



	ON_BN_CLICKED(IDC_SELECT_TV_EDGES_BUTTON, &CMFCUCLMI3SettingsDlg::OnBnClickedSelectTvEdgesButton)
	ON_BN_CLICKED(IDC_BUTTON_INFO_SELECT_TV_EDGES, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSelectTvEdges)
	ON_BN_CLICKED(IDC_BUTTON_INFO_SELECT_DISPLAYS, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSelectDisplays)

	ON_BN_CLICKED(IDC_BUTTON_INFO_RAIN_MODE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoRainMode)
	ON_BN_CLICKED(IDC_RAIN1, &CMFCUCLMI3SettingsDlg::OnBnClickedRain1)
	ON_BN_CLICKED(IDC_RAIN2, &CMFCUCLMI3SettingsDlg::OnBnClickedRain2)
	ON_BN_CLICKED(IDC_RAIN3, &CMFCUCLMI3SettingsDlg::OnBnClickedRain3)



	ON_BN_CLICKED(IDC_USE_CALIBRATION, &CMFCUCLMI3SettingsDlg::OnBnClickedUseCalibration)
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



	LPCWSTR pathConfigGeneral = pathConfigSGeneral.c_str();

	ifstream ifs_configGeneral(pathConfigGeneral);
	string content_configGeneral((istreambuf_iterator<char>(ifs_configGeneral)), (istreambuf_iterator<char>()));

	json general_settings = json::parse(content_configGeneral);
	//auto& general = myjson_config["general"];
	//auto& modules = myjson_config["modules"];

	// Set general settings data
	//globalSettingsDialogOpen = general_settings["view"]["open"]; //  keep window open
	globalShowFPS = general_settings["show_fps"]; // FPS
	globalCameraNr = general_settings["camera_nr"]; // CAMERA
	globalSelectedMode = general_settings["selected_mode"]; // selected mode
	globalUseCalibration = general_settings["use_calibration"]; // selected mode


	// Initializing an object of wstring
	wstring temp = wstring(globalSelectedMode.begin(), globalSelectedMode.end());

	// Applying c_str() method on temp
	LPCWSTR wideStringGlobalSelectedMode = temp.c_str();

	//string modesAvailable = general_settings["modes_available"]; // available modes

	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	// mode settings config data
	LPCWSTR pathConfigModes = pathConfigSModes.c_str();


	ifstream ifs_configModes(pathConfigModes);
	string content_configModes((istreambuf_iterator<char>(ifs_configModes)), (istreambuf_iterator<char>()));

	json mode_settings = json::parse(content_configModes);

	// Set mode settings data
	globalBlurAmount = mode_settings["blur"]["blur_amount"]; // blur amount
	globalSelectedSnowAmount = mode_settings["snow"]["snow_amount"]; // snow amount 
	globalSelectedRainAmount = mode_settings["rain"]["rain_mode"]; // snow amount 
	globalSettingsDialogOpen = mode_settings["keep_window_open"]; //  keep window open

	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	//WINDOW OPEN
	m_keepSettingsOpen.SetCheck(globalSettingsDialogOpen);
	//Use calibration
	m_useCalibration.SetCheck(globalUseCalibration);
	// FPS
	m_showFPS.SetWindowTextW(globalShowFPS ? L"ON" : L"OFF");
	// Camera
	for (int i = 0; i < MAX_CAMERA_INDEX; i++)
	{
		CString curIndex;
		curIndex.Format(_T("Camera %d"), i+1);
		m_camera.AddString(curIndex);
	}
	m_camera.SetCurSel(globalCameraNr);

	
	//Modes
	for (int i = 0; i < sizeof(modesAvailable) / sizeof(modesAvailable[0]); i++)
	{
		m_selectMode.AddString(modesAvailable[i]);
		if (modesAvailableStr[i] == globalSelectedMode)
		{
			globalSelectedModeNum = i;
		}
	}
	m_selectMode.SetCurSel(globalSelectedModeNum);
	



	
	//blur amount
	CString strSliderValue;
	m_blurAmount.SetRange(1, 250);
	m_blurAmount.SetPos(globalBlurAmount);
	strSliderValue.Format(_T("%d"), globalBlurAmount);
	m_blurAmountValue.SetWindowText(strSliderValue);

	//Snow mode - sets to the correct radio check based on the snow mode in the settings
	m_lightSnow.SetCheck(globalSelectedSnowAmount == "light_snow");
	m_mediumSnow.SetCheck(globalSelectedSnowAmount == "med_snow");
	m_harshSnow.SetCheck(globalSelectedSnowAmount == "harsh_snow");


	//Rain mode - sets to the correct radio check based on the rain mode in the settings
	m_drizzleRain.SetCheck(globalSelectedRainAmount == "drizzle");
	m_heavyRain.SetCheck(globalSelectedRainAmount == "heavy");
	m_torrentialRain.SetCheck(globalSelectedRainAmount == "torrential");

	return TRUE;  // return TRUE  unless you set the focus to a control
}



// Save 
void CMFCUCLMI3SettingsDlg::Save(){
	// Update values general settings
	globalCameraNr = m_camera.GetCurSel();
	globalSelectedModeNum = m_selectMode.GetCurSel();
	globalSelectedMode = modesAvailableStr[globalSelectedModeNum];

	

	LPCWSTR pathConfigGeneral = pathConfigSGeneral.c_str();
	ifstream ifs_config_general(pathConfigGeneral);
	string content_config_general((istreambuf_iterator<char>(ifs_config_general)), (istreambuf_iterator<char>()));
	json general_settings = json::parse(content_config_general);

	general_settings["show_fps"] = globalShowFPS;
	general_settings["camera_nr"] = globalCameraNr;
	general_settings["selected_mode"] = globalSelectedMode;
	general_settings["use_calibration"] = globalUseCalibration;
	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFileGeneral(pathConfigGeneral);
	outputConfigFileGeneral << setw(4) << general_settings << endl;




	// Update values mode settings
	globalBlurAmount = m_blurAmount.GetPos();

	LPCWSTR pathConfigMode = pathConfigSModes.c_str();
	ifstream ifs_config_mode(pathConfigMode);
	string content_config_mode((istreambuf_iterator<char>(ifs_config_mode)), (istreambuf_iterator<char>()));
	json mode_settings = json::parse(content_config_mode);

	mode_settings["blur"]["blur_amount"] = globalBlurAmount;
	mode_settings["snow"]["snow_amount"] = globalSelectedSnowAmount;
	mode_settings["rain"]["rain_mode"] = globalSelectedRainAmount;
	//for some reason i cannot have this setting in general settings. I do not know why. I fear this may be a problem with later settings. 
	mode_settings["keep_window_open"] = globalSettingsDialogOpen;
	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFileMode(pathConfigMode);
	outputConfigFileMode << setw(4) << mode_settings << endl;


	//Kill any existing versions of the app
	system("TASKKILL /IM UCL_Open-Illumiroom_V2.exe /T /F");

	// Run Illumiroom, with run argument
	ShellExecuteA(NULL, "open", runProgramPath, "run", NULL, SW_SHOWDEFAULT);

	//Add option on dialog to keep window open, or close automatically
	if (!globalSettingsDialogOpen)CDialogEx::OnOK();
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
	ShellExecute(NULL, NULL, aboutSite, NULL, NULL, SW_SHOWNORMAL);
	/*
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
	}*/
}


void CMFCUCLMI3SettingsDlg::OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar){
	CSliderCtrl* pSlider = reinterpret_cast<CSliderCtrl*>(pScrollBar);
	
	// Blur amount slider

	if (pSlider == &m_blurAmount) {
		CString strSliderValue;
		int iValue = m_blurAmount.GetPos(); // Get Slider value
		strSliderValue.Format(_T("%d"), iValue);
		m_blurAmountValue.SetWindowText(strSliderValue);
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



void CMFCUCLMI3SettingsDlg::OnBnClickedSelectDisplaysButton()
{
	// TODO: Add your control notification handler code here
	// 3. Run Illumiroom, with run argument
	ShellExecuteA(NULL, "open", runProgramPath, "display", NULL, SW_SHOWDEFAULT);
}

void CMFCUCLMI3SettingsDlg::OnBnClickedCalibrateSystemButton()
{
	// TODO: Add your control notification handler code here
	// Run Illumiroom, with background_capture argument
	ShellExecuteA(NULL, "open", runProgramPath, "calibration", NULL, SW_SHOWDEFAULT);
}


void CMFCUCLMI3SettingsDlg::OnBnClickedSelectTvEdgesButton()
{
	// Run Illumiroom, with select_tv argument
	ShellExecuteA(NULL, "open", runProgramPath, "select_tv", NULL, SW_SHOWDEFAULT);
}







void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFps()
{
	MessageBox(_T("FPS, or Frames per second, is the rate of frames (pictures) produced every second. The higher the number is, the smoother and better the interaction with the system will be. \n\nBy default, this setting is set to 'ON' meaning the FPS number shows at the top left corner of the projected screen. Changing this option to 'OFF' will hide the FPS number."), _T("FPS Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSelectDisplays()
{
	MessageBox(_T("This option allows you to select your two displays. Display windows will be shown for all connected displays, with a number next to them. For the TV and the Projector, please enter the corresponding number for the correct display"), _T("Display Selection Information"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCalibrateSystem()
{
	MessageBox(_T("The calibration system automatically runs a calibration program to ensure that the system is setup for your living room! \n\n For more detailed instructions and a video guide, please visit the software setup section on our website - https://expandedexperiences.com \n\n Place the webcam in the position where you will sit and play games or watch content - most likely on your sofa. The webcam should point towards your TV and the projection area. \n\n Then click the calibrate system button in the launcher; press 'y' if the correct output from the camera is shown.If not, press 'n', and select the next camera in the list, eg: 2 if you are currently on 1. \n\n Finally, allow the calibration system to run, and follow further instructions shown on screen."), _T("Display Selection Information"));
}






void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSelectTvEdges()
{
	MessageBox(_T("This option allows you to select the edges of your TV. Please draw a box around your TV by left clicking and holding, then let go. Finally press q to save'"), _T("Select TV Edges Information"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSelectMode()
{
	MessageBox(_T("This option allows you to chose the mode which you would like to use."), _T("Select Mode Information"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCamera()
{
	MessageBox(_T("Some computer devices may have two or more webcams available for UCL Open-Illumiroom V2 to use.  \n\nThe default webcam value is initially set to 1. If this is the incorrect webcam, chose 2, then 3 and so on. In most cases, changing 1 to 2 or 3 is likely to be a solution. \n If the incorrect camera is shown, simply close the window and try a different camera until the desired one is selected."), _T("Camera Information"));
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
	globalSelectedModeNum = m_selectMode.GetCurSel();
	globalSelectedMode = modesAvailableStr[globalSelectedModeNum];

	

	LPCWSTR pathConfig = pathConfigSGeneral.c_str();
	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));
	json general_settings = json::parse(content_config);

	general_settings["show_fps"] = globalShowFPS;
	general_settings["camera_nr"] = globalCameraNr;
	general_settings["selected_mode"] = globalSelectedMode;
	general_settings["keep_window_open"] = globalSettingsDialogOpen;
	general_settings["use_calibration"] = globalUseCalibration;


	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFile(pathConfig);
	outputConfigFile << setw(4) << general_settings << endl;


	// Update values mode settings
	globalBlurAmount = m_blurAmount.GetPos();


	LPCWSTR pathConfigMode = pathConfigSModes.c_str();
	ifstream ifs_config_mode(pathConfigMode);
	string content_config_mode((istreambuf_iterator<char>(ifs_config_mode)), (istreambuf_iterator<char>()));
	json mode_settings = json::parse(content_config_mode);

	mode_settings["blur"]["blur_amount"] = globalBlurAmount;
	mode_settings["snow"]["snow_amount"] = globalSelectedSnowAmount;
	mode_settings["keep_window_open"] = globalSettingsDialogOpen;
	mode_settings["rain"]["rain_mode"] = globalSelectedRainAmount;
	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFileMode(pathConfigMode);
	outputConfigFileMode << setw(4) << mode_settings << endl;


}






void CMFCUCLMI3SettingsDlg::OnBnClickedCloseprojector()
{
	// Kill system task
	system("TASKKILL /IM UCL_Open-Illumiroom_V2.exe /T /F");
}




void CMFCUCLMI3SettingsDlg::OnBnClickedStaticCameraOptions()
{
	// TODO: Add your control notification handler code here
}





void CMFCUCLMI3SettingsDlg::OnCbnSelchangeSelectModeCombo()
{
	// TODO: Add your control notification handler code here
}

void CMFCUCLMI3SettingsDlg::OnStnClickedStaticSelectMode()
{
	// TODO: Add your control notification handler code here
}








void CMFCUCLMI3SettingsDlg::OnStnClickedStaticBlurAmount()
{
	// TODO: Add your control notification handler code here
}





void CMFCUCLMI3SettingsDlg::OnEnChangeBlurAmountCounter()
{
	// TODO:  If this is a RICHEDIT control, the control will not
	// send this notification unless you override the CDialogEx::OnInitDialog()
	// function and call CRichEditCtrl().SetEventMask()
	// with the ENM_CHANGE flag ORed into the mask.

	// TODO:  Add your control notification handler code here
}


void CMFCUCLMI3SettingsDlg::OnBnClickedSnow1()
{
	// TODO: Add your control notification handler code here
	m_lightSnow.SetCheck(1);
	m_mediumSnow.SetCheck(0);
	m_harshSnow.SetCheck(0);
	globalSelectedSnowAmount = "light_snow";
}

void CMFCUCLMI3SettingsDlg::OnBnClickedSnow2()
{
	// TODO: Add your control notification handler code here
	m_lightSnow.SetCheck(0);
	m_mediumSnow.SetCheck(1);
	m_harshSnow.SetCheck(0);
	globalSelectedSnowAmount = "med_snow";
}

void CMFCUCLMI3SettingsDlg::OnBnClickedSnow3()
{
	// TODO: Add your control notification handler code here
	m_lightSnow.SetCheck(0);
	m_mediumSnow.SetCheck(0);
	m_harshSnow.SetCheck(1);
	globalSelectedSnowAmount = "harsh_snow";
}




void CMFCUCLMI3SettingsDlg::OnBnClickedKeepSettingsOpen()
{
	
	globalSettingsDialogOpen = m_keepSettingsOpen.GetCheck();
}

void CMFCUCLMI3SettingsDlg::OnBnClickedUseCalibration()
{
	globalUseCalibration = m_useCalibration.GetCheck();
}






void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoBlurAmount()
{
	MessageBox(_T("This option allows you to chose the amount of blurring in the blur mode."), _T("Blur amount information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSnowMode()
{
	MessageBox(_T("This option allows you to chose which snow mode you would like to use. For finer control over the modes, please check out the snow section of the mode_settings.json"), _T("Snow Mode information"));
}





void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoRainMode()
{
	MessageBox(_T("This option allows you to chose which rain mode you would like to use. For finer control over the modes, please check out the rain section of the mode_settings.json"), _T("Rain Mode information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedRain1()
{
	// TODO: Add your control notification handler code here
	m_drizzleRain.SetCheck(1);
	m_heavyRain.SetCheck(0);
	m_torrentialRain.SetCheck(0);
	globalSelectedRainAmount = "drizzle";
}


void CMFCUCLMI3SettingsDlg::OnBnClickedRain2()
{
	// TODO: Add your control notification handler code here
	m_drizzleRain.SetCheck(0);
	m_heavyRain.SetCheck(1);
	m_torrentialRain.SetCheck(0);
	globalSelectedRainAmount = "heavy";
}


void CMFCUCLMI3SettingsDlg::OnBnClickedRain3()
{
	// TODO: Add your control notification handler code here
	m_drizzleRain.SetCheck(0);
	m_heavyRain.SetCheck(0);
	m_torrentialRain.SetCheck(1);
	globalSelectedRainAmount = "torrential";
}







