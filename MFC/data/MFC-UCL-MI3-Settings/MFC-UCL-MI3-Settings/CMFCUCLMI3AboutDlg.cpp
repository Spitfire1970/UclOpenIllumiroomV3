// CMFCUCLMI3AboutDlg.cpp : implementation file
//

#include "pch.h"
#include "MFC-UCL-MI3-Settings.h"
#include "afxdialogex.h"
#include "CMFCUCLMI3AboutDlg.h"
#include <string>


// CAboutDlg dialog

IMPLEMENT_DYNAMIC(CMFCUCLMI3AboutDlg, CDialog)

CMFCUCLMI3AboutDlg::CMFCUCLMI3AboutDlg(CWnd* pParent /*=nullptr*/)
	: CDialog(IDD_MFCUCLMI3ABOUT_DIALOG, pParent)
{



}

CMFCUCLMI3AboutDlg::~CMFCUCLMI3AboutDlg()
{
}

void CMFCUCLMI3AboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);

	DDX_Control(pDX, IDC_ABOUT_CONTENT, m_about_content);
}

BEGIN_MESSAGE_MAP(CMFCUCLMI3AboutDlg, CDialog)
	//	ON_WM_ACTIVATE()
	ON_WM_CREATE()
END_MESSAGE_MAP()


void CMFCUCLMI3AboutDlg::InitAboutContent()
{
	std::wstring pathConfigS = L"data\\about\\about.txt";
	LPCWSTR pAboutFile = pathConfigS.c_str();

	CStdioFile file(pAboutFile, CFile::modeRead);

	CString line;

	while (file.ReadString(line))
	{
		m_about_content.AddString(line);
	}

	m_about_content.SetHorizontalExtent(1000);
}


// Init
BOOL CMFCUCLMI3AboutDlg::OnInitDialog() {
	CDialog::OnInitDialog();

	InitAboutContent();

	return TRUE;
}

