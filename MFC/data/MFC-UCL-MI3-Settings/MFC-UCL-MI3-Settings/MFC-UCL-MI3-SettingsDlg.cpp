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
bool globalLowLight;
int globalMouseEye;
bool globalSettingsDialogOpen;

//mode settings
int globalBlurAmount;
string globalSelectedSnowAmount;

string globalSelectedMode;
int globalSelectedModeNum = 0;

string modesAvailableStr[] = { "blur","wobble","cartoon","snow","rain","low_health","speed_lines" };
LPCWSTR  modesAvailable[] = { L"blur",L"wobble",L"cartoon",L"snow",L"rain",L"low_health",L"speed_lines" };




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

	DDX_Control(pDX, IDC_BLUR_AMOUNT_SLIDER, m_blurAmount);
	DDX_Control(pDX, IDC_BLUR_AMOUNT_COUNTER, m_blurAmountValue);
	DDX_Control(pDX, IDC_FPS_BUTTON, m_showFPS);
	DDX_Control(pDX, IDC_LOW_LIGHT_BUTTON, m_lowLightOn);
	DDX_Control(pDX, IDC_SELECT_MODE_COMBO, m_selectMode);
	DDX_Control(pDX, IDC_KEEP_SETTINGS_OPEN, m_keepSettingsOpen);

	DDX_Control(pDX, IDC_SNOW1, m_lightSnow);
	DDX_Control(pDX, IDC_SNOW2, m_mediumSnow);
	DDX_Control(pDX, IDC_SNOW3, m_harshSnow);

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
	ON_BN_CLICKED(IDC_BUTTON_INFO_SNOW_MODE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSnowMode)
	ON_BN_CLICKED(IDC_BUTTON_INFO_BLUR_AMOUNT, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoBlurAmount)
	ON_BN_CLICKED(IDC_SELECT_DISPLAYS_BUTTON, &CMFCUCLMI3SettingsDlg::OnBnClickedSelectDisplaysButton)
	ON_BN_CLICKED(IDCLOSEPROJECTOR, &CMFCUCLMI3SettingsDlg::OnBnClickedCloseprojector)
	ON_BN_CLICKED(IDC_STATIC_CAMERA_OPTIONS, &CMFCUCLMI3SettingsDlg::OnBnClickedStaticCameraOptions)
	ON_CBN_SELCHANGE(IDC_SELECT_MODE_COMBO, &CMFCUCLMI3SettingsDlg::OnCbnSelchangeSelectModeCombo)
	ON_BN_CLICKED(IDC_BUTTON_INFO_SELECT_MODE, &CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSelectMode)
	ON_STN_CLICKED(IDC_STATIC_SELECT_MODE, &CMFCUCLMI3SettingsDlg::OnStnClickedStaticSelectMode)

	ON_BN_CLICKED(IDC_SNOW1, &CMFCUCLMI3SettingsDlg::OnBnClickedSnow1)
	ON_BN_CLICKED(IDC_SNOW2, &CMFCUCLMI3SettingsDlg::OnBnClickedSnow2)
	ON_BN_CLICKED(IDC_SNOW3, &CMFCUCLMI3SettingsDlg::OnBnClickedSnow3)
	ON_BN_CLICKED(IDC_KEEP_SETTINGS_OPEN, &CMFCUCLMI3SettingsDlg::OnBnClickedKeepSettingsOpen)

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


	// general settings config data
	wstring pathConfigSGeneral = L"main.dist\\settings\\general_settings.json";
	LPCWSTR pathConfigGeneral = pathConfigSGeneral.c_str();


	ifstream ifs_configGeneral(pathConfigGeneral);
	string content_configGeneral((istreambuf_iterator<char>(ifs_configGeneral)), (istreambuf_iterator<char>()));

	json general_settings = json::parse(content_configGeneral);
	//auto& general = myjson_config["general"];
	//auto& modules = myjson_config["modules"];

	// Set general settings data
	//globalSettingsDialogOpen = general_settings["view"]["open"]; //  keep window open
	globalShowFPS = general_settings["show_fps"]; // FPS
	globalLowLight = general_settings["view"]["low_light_indicator_on"]; // LIGHT
	globalCameraNr = general_settings["camera"]["camera_nr"]; // CAMERA
	globalSelectedMode = general_settings["selected_mode"]; // selected mode
	

	// Initializing an object of wstring
	wstring temp = wstring(globalSelectedMode.begin(), globalSelectedMode.end());

	// Applying c_str() method on temp
	LPCWSTR wideStringGlobalSelectedMode = temp.c_str();

	//string modesAvailable = general_settings["modes_available"]; // available modes

	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	// mode settings config data
	wstring pathConfigSModes = L"main.dist\\settings\\mode_settings.json";
	LPCWSTR pathConfigModes = pathConfigSModes.c_str();


	ifstream ifs_configModes(pathConfigModes);
	string content_configModes((istreambuf_iterator<char>(ifs_configModes)), (istreambuf_iterator<char>()));

	json mode_settings = json::parse(content_configModes);

	// Set mode settings data
	globalBlurAmount = mode_settings["blur"]["blur_amount"]; // blur amount
	globalSelectedSnowAmount = mode_settings["snow"]["snow_amount"]; // snow amount 
	globalSettingsDialogOpen = mode_settings["keep_window_open"]; //  keep window open

	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	//WINDOW OPEN
	m_keepSettingsOpen.SetCheck(globalSettingsDialogOpen);
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

	return TRUE;  // return TRUE  unless you set the focus to a control
}



// Save 
void CMFCUCLMI3SettingsDlg::Save(){
	// Update values general settings
	globalCameraNr = m_camera.GetCurSel();
	globalSelectedModeNum = m_selectMode.GetCurSel();
	globalSelectedMode = modesAvailableStr[globalSelectedModeNum];

	
	wstring StrConfigGeneral = L"main.dist\\settings\\general_settings.json";
	LPCWSTR pathConfigGeneral = StrConfigGeneral.c_str();
	ifstream ifs_config_general(pathConfigGeneral);
	string content_config_general((istreambuf_iterator<char>(ifs_config_general)), (istreambuf_iterator<char>()));
	json general_settings = json::parse(content_config_general);

	general_settings["show_fps"] = globalShowFPS;
	general_settings["view"]["low_light_indicator_on"] = globalLowLight;
	general_settings["camera"]["camera_nr"] = globalCameraNr;
	general_settings["selected_mode"] = globalSelectedMode;
	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFileGeneral(pathConfigGeneral);
	outputConfigFileGeneral << setw(4) << general_settings << endl;




	// Update values mode settings
	globalBlurAmount = m_blurAmount.GetPos();

	wstring StrConfigMode = L"main.dist\\settings\\mode_settings.json";
	LPCWSTR pathConfigMode = StrConfigMode.c_str();
	ifstream ifs_config_mode(pathConfigMode);
	string content_config_mode((istreambuf_iterator<char>(ifs_config_mode)), (istreambuf_iterator<char>()));
	json mode_settings = json::parse(content_config_mode);

	mode_settings["blur"]["blur_amount"] = globalBlurAmount;
	mode_settings["snow"]["snow_amount"] = globalSelectedSnowAmount;
	//for some reason i cannot have this setting in general settings. I do not know why. I fear this may be a problem with later settings. 
	mode_settings["keep_window_open"] = globalSettingsDialogOpen;
	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFileMode(pathConfigMode);
	outputConfigFileMode << setw(4) << mode_settings << endl;


	//Kill any existing versions of the app
	system("TASKKILL /IM main.exe");

	// Run Illumiroom, with run argument
	ShellExecuteA(NULL, "open", "main.dist\\main.exe", "run", NULL, SW_SHOWDEFAULT);

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

void CMFCUCLMI3SettingsDlg::OnBnClickedSelectDisplaysButton()
{
	// TODO: Add your control notification handler code here
	// 3. Run Illumiroom, with run argument
	ShellExecuteA(NULL, "open", "main.dist\\main.exe", "display", NULL, SW_SHOWDEFAULT);
}







void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoFps()
{
	MessageBox(_T("FPS, or Frames per second, is the rate of frames (pictures) produced every second. The higher the number is, the smoother and better the interaction with the system will be. \n\nBy default, this setting is set to 'ON' meaning the FPS number shows at the top left corner of the projected screen. Changing this option to 'OFF' will hide the FPS number."), _T("FPS Information"));
}

void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoLight()
{
    MessageBox(_T("Using MotionInput in a place with low lighting can cause visual control commands to not be recognised accordingly.In this case, setting Low Light option 'ON' is likely to improve interaction with MotionInput.\n\nThe Low Light indicator is set to'OFF' by default."), _T("Low Light Information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoCamera()
{
    MessageBox(_T("Some computer devices may have two or more webcams available for MotionInput to use (such as Microsoft Surface devices which often have a front and a rear camera). Some users might also prefer attaching an additional camera(s) to their computer devices. \n\nThe default camera value is initially set to 0. If you are experiencing difficulties with MotionInput camera detection, set this option to a different number. In most cases, changing 0 to 1 or 2 is likely to be a solution. \nRestart MotionInput to check if the new number selected has resolved the problem. If not adjust the setting again until MotionInput is connected to the desired camera."), _T("Default Camera Information"));
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

	
	wstring tempStrConfig = L"main.dist\\settings\\general_settings.json";
	LPCWSTR pathConfig = tempStrConfig.c_str();
	ifstream ifs_config(pathConfig);
	string content_config((istreambuf_iterator<char>(ifs_config)), (istreambuf_iterator<char>()));
	json general_settings = json::parse(content_config);

	general_settings["show_fps"] = globalShowFPS;
	general_settings["view"]["low_light_indicator_on"] = globalLowLight;
	general_settings["camera"]["camera_nr"] = globalCameraNr;
	general_settings["eye"]["Eye_mouse_speed"] = globalMouseEye;
	general_settings["selected_mode"] = globalSelectedMode;
	general_settings["keep_window_open"] = globalSettingsDialogOpen;


	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFile(pathConfig);
	outputConfigFile << setw(4) << general_settings << endl;


	// Update values mode settings
	globalBlurAmount = m_blurAmount.GetPos();

	wstring StrConfigMode = L"main.dist\\settings\\mode_settings.json";
	LPCWSTR pathConfigMode = StrConfigMode.c_str();
	ifstream ifs_config_mode(pathConfigMode);
	string content_config_mode((istreambuf_iterator<char>(ifs_config_mode)), (istreambuf_iterator<char>()));
	json mode_settings = json::parse(content_config_mode);

	mode_settings["blur"]["blur_amount"] = globalBlurAmount;
	mode_settings["snow"]["snow_amount"] = globalSelectedSnowAmount;
	mode_settings["keep_window_open"] = globalSettingsDialogOpen;
	// WRITE INTO CONFIG JSON ALL CHANGES
	ofstream outputConfigFileMode(pathConfigMode);
	outputConfigFileMode << setw(4) << mode_settings << endl;


}






void CMFCUCLMI3SettingsDlg::OnBnClickedCloseprojector()
{
	// TODO: repplace main.exe with different name for illumiroom

	system("TASKKILL /IM main.exe");
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


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSelectMode()
{
	MessageBox(_T("This option allows you to chose the mode which you would like to use."), _T("Select Mode Information"));
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
	// TODO: Add your control notification handler code here
	globalSettingsDialogOpen = m_keepSettingsOpen.GetCheck();
}





void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoBlurAmount()
{
	MessageBox(_T("This option allows you to chose the amount of blurring in the blur mode."), _T("Blur amount information"));
}


void CMFCUCLMI3SettingsDlg::OnBnClickedButtonInfoSnowMode()
{
	MessageBox(_T("This option allows you to chose which snow mode you would like to use. For finer control over modes, please check out the snow section of the mode_settings.json"), _T("Snow Mode information"));
}
