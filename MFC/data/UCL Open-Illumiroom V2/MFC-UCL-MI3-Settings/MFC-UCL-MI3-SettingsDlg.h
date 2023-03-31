// MFC-UCL-MI3-SettingsDlg.h : HEADER FILE


#include "CMFCUCLMI3AboutDlg.h"

#pragma once


// CMFCUCLMI3SettingsDlg dialog
class CMFCUCLMI3SettingsDlg : public CDialogEx
{

// Construction
public:
	CMFCUCLMI3SettingsDlg(CWnd* pParent = nullptr);	// standard constructor

// Dialog Data
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_MFCUCLMI3SETTINGS_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()

public:
	afx_msg void ShowAbout();
	afx_msg void ShowHelp();
	afx_msg void Save();

	CComboBox m_mode;
	CComboBox m_method;
	CComboBox m_selectMode;

	CButton m_showFPS;
	CButton m_lowLightOn;
	CButton m_keepSettingsOpen;
	CButton m_useCalibration;
	afx_msg void UpdateShowFPS();
	afx_msg void UpdateLowLight();

	CComboBox m_camera;

	// Just keep this here in case we want to use it?
	// CEdit m_cameraValue;

	CSliderCtrl m_blurAmount;
	CEdit m_blurAmountValue;

	CSliderCtrl m_soundThresholdAmount;
	CEdit m_soundThresholdAmountValue;

	CButton m_lightSnow;
	CButton m_mediumSnow;
	CButton m_harshSnow;

	CButton m_drizzleRain;
	CButton m_heavyRain;
	CButton m_torrentialRain;


	afx_msg void OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar);
	
	CComboBox m_smile;
	CComboBox m_fishFace;
	CComboBox m_raisedEyebrows;
	CComboBox m_openMouth;
	CButton m_modeNose;
	CButton m_modeEyes;
	CButton m_methodFacial;
	CButton m_methodSpeech;
	afx_msg void UpdateModeNose();
	afx_msg void UpdateModeEyes();
	afx_msg void UpdateMethodFacial();
	afx_msg void UpdateMethodSpeech();
	CComboBox m_rotationRight;
	CComboBox m_rotationLeft;
	CSliderCtrl m_noseBoxBond;
	CEdit m_noseBoxBondValue;
    afx_msg void OnBnClickedButtonInfoMode();
    afx_msg void OnBnClickedButtonInfoMethod();
    afx_msg void OnBnClickedButtonInfoFps();
    afx_msg void OnBnClickedButtonInfoLight();
    afx_msg void OnBnClickedButtonInfoCamera();
    afx_msg void OnBnClickedButtonInfoNoseMouse();
    afx_msg void OnBnClickedButtonInfoNoseboxBound();
    afx_msg void OnBnClickedButtonInfoEyesMouse();
    afx_msg void OnBnClickedButtonInfoSmile();
    afx_msg void OnBnClickedButtonInfoFishface();
    afx_msg void OnBnClickedButtonInfoEyebrows();
    afx_msg void OnBnClickedButtonInfoOpenMouth();
    afx_msg void OnBnClickedButtonInfoRotateHeadLeft();
    afx_msg void OnBnClickedButtonInfoRotateHeadRight();

	CMFCUCLMI3AboutDlg m_aboutDlg;
	afx_msg void OnStnClickedStaticNoseboxBound2();
	afx_msg void OnBnClickedI();
	afx_msg void OnCbnSelchangeOpenMouthCombo();
	afx_msg void OnCbnSelchangeDefaultcameraCombo();
	afx_msg void OnBnClickedCancel();
	afx_msg void OnBnClickedOk2();
	afx_msg void OnBnClickedYes();
	afx_msg void OnBnClickedSaveonly();
	afx_msg void OnBnClickedFpsButton2();
	afx_msg void OnBnClickedSelectDisplaysButton();
	afx_msg void OnBnClickedCloseprojector();
	afx_msg void OnBnClickedSaveonly2();
	afx_msg void OnBnClickedStaticCameraOptions();
	afx_msg void OnBnClickedButtonInfoCamera2();
	afx_msg void OnCbnSelchangeSelectModeCombo();
	afx_msg void OnBnClickedButtonInfoSelectMode();
	afx_msg void OnStnClickedStaticSelectMode();
	afx_msg void OnStnClickedStaticBlurAmount();
	afx_msg void OnNMCustomdrawBlurAmountSlider(NMHDR* pNMHDR, LRESULT* pResult);
	afx_msg void OnEnChangeBlurAmountCounter();
	afx_msg void OnBnClickedCheck1();
	afx_msg void OnBnClickedAdvancedOptions2();
	afx_msg void OnBnClickedSnow3();
	afx_msg void OnBnClickedSnow2();
	afx_msg void OnBnClickedKeepSettingsOpen();
	afx_msg void OnBnClickedSnow1();
	afx_msg void OnBnClickedButtonInfoBlurAmount();
	afx_msg void OnBnClickedButtonInfoSnowMode();
	afx_msg void OnBnClickedButtonInfoBackgroundCapture();
	afx_msg void OnBnClickedBackgroundCaptureButton();
	afx_msg void OnBnClickedButtonInfoSelectDisplays3();
	afx_msg void OnBnClickedSelectDisplaysButton3();
	afx_msg void OnBnClickedSelectTvEdgesButton();
	afx_msg void OnBnClickedButtonInfoSelectTvEdges();
	afx_msg void OnBnClickedButtonInfoSelectDisplays();
	afx_msg void OnBnClickedSnowBox2();
	afx_msg void OnBnClickedButtonInfoRainMode();
	afx_msg void OnBnClickedRain1();
	afx_msg void OnBnClickedRain2();
	afx_msg void OnBnClickedRain3();
	afx_msg void OnBnClickedCalibrateSystemButton();
	afx_msg void OnBnClickedButtonInfoCalibrateSystem();
	afx_msg void OnStnClickedStaticCalibrateSystem();
	afx_msg void OnBnClickedUseCalibration();
	afx_msg void OnBnClickedButtonInfoSoundThreshold();
};

