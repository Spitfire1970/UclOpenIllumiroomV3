
// MFC-UCL-MI3-Settings.h : main header file for the PROJECT_NAME application
//

#pragma once

#ifndef __AFXWIN_H__
	#error "include 'pch.h' before including this file for PCH"
#endif

#include "resource.h"		// main symbols


// CMFCUCLMI3SettingsApp:
// See MFC-UCL-MI3-Settings.cpp for the implementation of this class
//

class CMFCUCLMI3SettingsApp : public CWinApp
{
public:
	CMFCUCLMI3SettingsApp();

// Overrides
public:
	virtual BOOL InitInstance();

// Implementation

	DECLARE_MESSAGE_MAP()
};

extern CMFCUCLMI3SettingsApp theApp;

