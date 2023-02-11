#pragma once
#include "afxdialogex.h"

class CMFCUCLMI3AboutDlg : public CDialog
{
	DECLARE_DYNAMIC(CMFCUCLMI3AboutDlg)

protected:
	void InitAboutContent();
	BOOL OnInitDialog();
public:
	CMFCUCLMI3AboutDlg(CWnd* pParent = nullptr);   // standard constructor
	virtual ~CMFCUCLMI3AboutDlg();

	// Dialog Data
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_MFCUCLMI3ABOUT_DIALOG };
#endif

protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	DECLARE_MESSAGE_MAP()
public:
	CListBox m_about_content;
	afx_msg void OnLbnSelchangeAdvancedOptions();
};
