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

	CButton m_showFPS;
	CButton m_lowLightOn;
	afx_msg void UpdateShowFPS();
	afx_msg void UpdateLowLight();

	CComboBox m_camera;
	// Just keep this here in case we want to use it?
	// CEdit m_cameraValue;

	CSliderCtrl m_noseMouseSpeed;
	CEdit m_noseMouseSpeedValue;
	CSliderCtrl m_eyesMouseSpeed;
	CEdit m_eyesMouseSpeedValue;

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
};

