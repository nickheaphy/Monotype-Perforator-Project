#tag DesktopWindow
Begin DesktopWindow MainUI
   Backdrop        =   0
   BackgroundColor =   &cFFFFFF
   Composite       =   False
   DefaultLocation =   2
   FullScreen      =   False
   HasBackgroundColor=   False
   HasCloseButton  =   True
   HasFullScreenButton=   False
   HasMaximizeButton=   True
   HasMinimizeButton=   True
   Height          =   400
   ImplicitInstance=   True
   MacProcID       =   0
   MaximumHeight   =   32000
   MaximumWidth    =   32000
   MenuBar         =   1599762431
   MenuBarVisible  =   False
   MinimumHeight   =   64
   MinimumWidth    =   64
   Resizeable      =   True
   Title           =   "Perforator Punch"
   Type            =   0
   Visible         =   True
   Width           =   550
   Begin DesktopLabel Label1
      AllowAutoDeactivate=   True
      Bold            =   False
      Enabled         =   True
      FontName        =   "System"
      FontSize        =   0.0
      FontUnit        =   0
      Height          =   20
      Index           =   -2147483648
      Italic          =   False
      Left            =   20
      LockBottom      =   False
      LockedInPosition=   False
      LockLeft        =   True
      LockRight       =   False
      LockTop         =   True
      Multiline       =   False
      Scope           =   0
      Selectable      =   False
      TabIndex        =   0
      TabPanelIndex   =   0
      TabStop         =   True
      Text            =   "Perforator Interface:"
      TextAlignment   =   0
      TextColor       =   &c000000
      Tooltip         =   ""
      Top             =   20
      Transparent     =   False
      Underline       =   False
      Visible         =   True
      Width           =   140
   End
   Begin DesktopPopupMenu DevicesPopupMenu
      AllowAutoDeactivate=   True
      Bold            =   False
      Enabled         =   True
      FontName        =   "System"
      FontSize        =   0.0
      FontUnit        =   0
      Height          =   20
      Index           =   -2147483648
      InitialValue    =   ""
      Italic          =   False
      Left            =   172
      LockBottom      =   False
      LockedInPosition=   False
      LockLeft        =   True
      LockRight       =   False
      LockTop         =   True
      Scope           =   0
      SelectedRowIndex=   0
      TabIndex        =   1
      TabPanelIndex   =   0
      TabStop         =   True
      Tooltip         =   ""
      Top             =   20
      Transparent     =   False
      Underline       =   False
      Visible         =   True
      Width           =   246
   End
   Begin DesktopButton ConnectButton
      AllowAutoDeactivate=   True
      Bold            =   False
      Cancel          =   False
      Caption         =   "Connect"
      Default         =   True
      Enabled         =   False
      FontName        =   "System"
      FontSize        =   0.0
      FontUnit        =   0
      Height          =   20
      Index           =   -2147483648
      Italic          =   False
      Left            =   450
      LockBottom      =   False
      LockedInPosition=   False
      LockLeft        =   True
      LockRight       =   False
      LockTop         =   True
      MacButtonStyle  =   0
      Scope           =   0
      TabIndex        =   2
      TabPanelIndex   =   0
      TabStop         =   True
      Tooltip         =   ""
      Top             =   20
      Transparent     =   False
      Underline       =   False
      Visible         =   True
      Width           =   80
   End
   Begin Timer LookForSerialDevices
      Enabled         =   True
      Index           =   -2147483648
      LockedInPosition=   False
      Period          =   1000
      RunMode         =   2
      Scope           =   0
      TabPanelIndex   =   0
   End
   Begin SerialConnection PunchConnection
      Baud            =   8
      Bits            =   3
      CTS             =   False
      DTR             =   False
      Index           =   -2147483648
      LockedInPosition=   False
      Parity          =   0
      Scope           =   0
      StopBit         =   0
      TabPanelIndex   =   0
      XON             =   False
   End
   Begin DesktopTextArea SerialOut
      AllowAutoDeactivate=   True
      AllowFocusRing  =   True
      AllowSpellChecking=   True
      AllowStyledText =   True
      AllowTabs       =   False
      BackgroundColor =   &cFFFFFF
      Bold            =   False
      Enabled         =   True
      FontName        =   "System"
      FontSize        =   0.0
      FontUnit        =   0
      Format          =   ""
      HasBorder       =   True
      HasHorizontalScrollbar=   False
      HasVerticalScrollbar=   True
      Height          =   94
      HideSelection   =   True
      Index           =   -2147483648
      Italic          =   False
      Left            =   20
      LineHeight      =   0.0
      LineSpacing     =   1.0
      LockBottom      =   False
      LockedInPosition=   False
      LockLeft        =   True
      LockRight       =   False
      LockTop         =   True
      MaximumCharactersAllowed=   0
      Multiline       =   True
      ReadOnly        =   True
      Scope           =   0
      TabIndex        =   3
      TabPanelIndex   =   0
      TabStop         =   True
      Text            =   ""
      TextAlignment   =   0
      TextColor       =   &c000000
      Tooltip         =   ""
      Top             =   286
      Transparent     =   False
      Underline       =   False
      UnicodeMode     =   1
      ValidationMask  =   ""
      Visible         =   True
      Width           =   510
   End
   Begin DesktopGroupBox PunchTools
      AllowAutoDeactivate=   True
      Bold            =   False
      Caption         =   "Punch Tape"
      Enabled         =   False
      FontName        =   "System"
      FontSize        =   0.0
      FontUnit        =   0
      Height          =   211
      Index           =   -2147483648
      Italic          =   False
      Left            =   20
      LockBottom      =   False
      LockedInPosition=   False
      LockLeft        =   True
      LockRight       =   False
      LockTop         =   True
      Scope           =   0
      TabIndex        =   4
      TabPanelIndex   =   0
      TabStop         =   True
      Tooltip         =   ""
      Top             =   63
      Transparent     =   False
      Underline       =   False
      Visible         =   True
      Width           =   266
      Begin DesktopButton LoadAndSendButton
         AllowAutoDeactivate=   True
         Bold            =   False
         Cancel          =   False
         Caption         =   "Load and Send Tape"
         Default         =   True
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   40
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MacButtonStyle  =   0
         Scope           =   0
         TabIndex        =   0
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   234
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         Width           =   202
      End
      Begin DesktopTextField PunchDelay
         AllowAutoDeactivate=   True
         AllowFocusRing  =   True
         AllowSpellChecking=   False
         AllowTabs       =   False
         BackgroundColor =   &cFFFFFF
         Bold            =   False
         Enabled         =   False
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Format          =   ""
         HasBorder       =   True
         Height          =   22
         Hint            =   "This is the delay between punches in milliseconds"
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   170
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MaximumCharactersAllowed=   0
         Password        =   False
         ReadOnly        =   False
         Scope           =   0
         TabIndex        =   2
         TabPanelIndex   =   0
         TabStop         =   True
         Text            =   "30"
         TextAlignment   =   0
         TextColor       =   &c000000
         Tooltip         =   ""
         Top             =   99
         Transparent     =   False
         Underline       =   False
         ValidationMask  =   "##9"
         Visible         =   True
         Width           =   80
      End
      Begin DesktopTextField ForwardDelay
         AllowAutoDeactivate=   True
         AllowFocusRing  =   True
         AllowSpellChecking=   False
         AllowTabs       =   False
         BackgroundColor =   &cFFFFFF
         Bold            =   False
         Enabled         =   False
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Format          =   ""
         HasBorder       =   True
         Height          =   22
         Hint            =   "This is the delay between tape advance in milliseconds"
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   170
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MaximumCharactersAllowed=   0
         Password        =   False
         ReadOnly        =   False
         Scope           =   0
         TabIndex        =   4
         TabPanelIndex   =   0
         TabStop         =   True
         Text            =   "100"
         TextAlignment   =   0
         TextColor       =   &c000000
         Tooltip         =   ""
         Top             =   131
         Transparent     =   False
         Underline       =   False
         ValidationMask  =   "##9"
         Visible         =   True
         Width           =   80
      End
      Begin DesktopCheckBox PunchDelayCB
         AllowAutoDeactivate=   True
         Bold            =   False
         Caption         =   "Punch Delay"
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   40
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         Scope           =   0
         TabIndex        =   5
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   "Enable the setting of the punch delay"
         Top             =   99
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         VisualState     =   0
         Width           =   100
      End
      Begin DesktopCheckBox ForwardDelayCB
         AllowAutoDeactivate=   True
         Bold            =   False
         Caption         =   "Forward Delay"
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   40
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         Scope           =   0
         TabIndex        =   6
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   "Enable the setting of the forward delay"
         Top             =   133
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         VisualState     =   0
         Width           =   118
      End
      Begin DesktopTextField Header
         AllowAutoDeactivate=   True
         AllowFocusRing  =   True
         AllowSpellChecking=   False
         AllowTabs       =   False
         BackgroundColor =   &cFFFFFF
         Bold            =   False
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Format          =   ""
         HasBorder       =   True
         Height          =   22
         Hint            =   ""
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   170
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MaximumCharactersAllowed=   0
         Password        =   False
         ReadOnly        =   False
         Scope           =   0
         TabIndex        =   7
         TabPanelIndex   =   0
         TabStop         =   True
         Text            =   "400"
         TextAlignment   =   0
         TextColor       =   &c000000
         Tooltip         =   ""
         Top             =   165
         Transparent     =   False
         Underline       =   False
         ValidationMask  =   "999"
         Visible         =   True
         Width           =   80
      End
      Begin DesktopCheckBox HeaderLabel
         AllowAutoDeactivate=   True
         Bold            =   False
         Caption         =   "Header (mm)"
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   40
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         Scope           =   0
         TabIndex        =   8
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   165
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         VisualState     =   1
         Width           =   100
      End
      Begin DesktopCheckBox FooterLabel
         AllowAutoDeactivate=   True
         Bold            =   False
         Caption         =   "Footer (mm)"
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   40
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         Scope           =   0
         TabIndex        =   9
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   197
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         VisualState     =   1
         Width           =   100
      End
      Begin DesktopTextField Footer
         AllowAutoDeactivate=   True
         AllowFocusRing  =   True
         AllowSpellChecking=   False
         AllowTabs       =   False
         BackgroundColor =   &cFFFFFF
         Bold            =   False
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Format          =   ""
         HasBorder       =   True
         Height          =   22
         Hint            =   ""
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   170
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MaximumCharactersAllowed=   0
         Password        =   False
         ReadOnly        =   False
         Scope           =   0
         TabIndex        =   10
         TabPanelIndex   =   0
         TabStop         =   True
         Text            =   "400"
         TextAlignment   =   0
         TextColor       =   &c000000
         Tooltip         =   ""
         Top             =   195
         Transparent     =   False
         Underline       =   False
         ValidationMask  =   "999"
         Visible         =   True
         Width           =   80
      End
      Begin DesktopBevelButton StopButton
         AllowAutoDeactivate=   True
         AllowFocus      =   True
         BackgroundColor =   &cFF000300
         BevelStyle      =   5
         Bold            =   False
         ButtonStyle     =   0
         Caption         =   ""
         CaptionAlignment=   3
         CaptionDelta    =   0
         CaptionPosition =   1
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         HasBackgroundColor=   True
         Height          =   22
         Icon            =   0
         IconAlignment   =   1
         IconDeltaX      =   0
         IconDeltaY      =   0
         Index           =   -2147483648
         InitialParent   =   "PunchTools"
         Italic          =   False
         Left            =   254
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MenuStyle       =   0
         Scope           =   0
         TabIndex        =   11
         TabPanelIndex   =   0
         TabStop         =   True
         TextColor       =   &c00000000
         Tooltip         =   ""
         Top             =   234
         Transparent     =   True
         Underline       =   False
         Value           =   False
         Visible         =   True
         Width           =   24
      End
   End
   Begin DesktopGroupBox PunchTests
      AllowAutoDeactivate=   True
      Bold            =   False
      Caption         =   "Punch Tests"
      Enabled         =   False
      FontName        =   "System"
      FontSize        =   0.0
      FontUnit        =   0
      Height          =   211
      Index           =   -2147483648
      Italic          =   False
      Left            =   298
      LockBottom      =   False
      LockedInPosition=   False
      LockLeft        =   True
      LockRight       =   False
      LockTop         =   True
      Scope           =   0
      TabIndex        =   5
      TabPanelIndex   =   0
      TabStop         =   True
      Tooltip         =   ""
      Top             =   63
      Transparent     =   False
      Underline       =   False
      Visible         =   True
      Width           =   232
      Begin DesktopButton Test1
         AllowAutoDeactivate=   True
         Bold            =   False
         Cancel          =   False
         Caption         =   "Test 1"
         Default         =   False
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTests"
         Italic          =   False
         Left            =   318
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MacButtonStyle  =   0
         Scope           =   0
         TabIndex        =   0
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   90
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         Width           =   80
      End
      Begin DesktopButton Test2
         AllowAutoDeactivate=   True
         Bold            =   False
         Cancel          =   False
         Caption         =   "Test 2"
         Default         =   False
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTests"
         Italic          =   False
         Left            =   430
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MacButtonStyle  =   0
         Scope           =   0
         TabIndex        =   1
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   90
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         Width           =   80
      End
      Begin DesktopButton Test3
         AllowAutoDeactivate=   True
         Bold            =   False
         Cancel          =   False
         Caption         =   "Test 3"
         Default         =   False
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTests"
         Italic          =   False
         Left            =   318
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MacButtonStyle  =   0
         Scope           =   0
         TabIndex        =   2
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   122
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         Width           =   80
      End
      Begin DesktopButton Test4
         AllowAutoDeactivate=   True
         Bold            =   False
         Cancel          =   False
         Caption         =   "Test 4"
         Default         =   False
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTests"
         Italic          =   False
         Left            =   430
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MacButtonStyle  =   0
         Scope           =   0
         TabIndex        =   3
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   122
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         Width           =   80
      End
      Begin DesktopButton TapeAdvance
         AllowAutoDeactivate=   True
         Bold            =   False
         Cancel          =   False
         Caption         =   "Advance"
         Default         =   False
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTests"
         Italic          =   False
         Left            =   430
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MacButtonStyle  =   0
         Scope           =   0
         TabIndex        =   4
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   154
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         Width           =   80
      End
      Begin DesktopButton TapeRetract
         AllowAutoDeactivate=   True
         Bold            =   False
         Cancel          =   False
         Caption         =   "Retract"
         Default         =   False
         Enabled         =   True
         FontName        =   "System"
         FontSize        =   0.0
         FontUnit        =   0
         Height          =   20
         Index           =   -2147483648
         InitialParent   =   "PunchTests"
         Italic          =   False
         Left            =   430
         LockBottom      =   False
         LockedInPosition=   False
         LockLeft        =   True
         LockRight       =   False
         LockTop         =   True
         MacButtonStyle  =   0
         Scope           =   0
         TabIndex        =   5
         TabPanelIndex   =   0
         TabStop         =   True
         Tooltip         =   ""
         Top             =   186
         Transparent     =   False
         Underline       =   False
         Visible         =   True
         Width           =   80
      End
   End
   Begin Thread sendTapeData
      Index           =   -2147483648
      LockedInPosition=   False
      Priority        =   5
      Scope           =   0
      StackSize       =   0
      TabPanelIndex   =   0
   End
End
#tag EndDesktopWindow

#tag WindowCode
	#tag Event
		Sub Closing()
		  Quit
		End Sub
	#tag EndEvent

	#tag Event
		Sub Opening()
		  me.Title = me.title + " v" + app.MajorVersion.ToString + "." + app.MinorVersion.ToString + "." + app.BugVersion.ToString
		  
		End Sub
	#tag EndEvent


	#tag Method, Flags = &h0
		Sub serialoutappend(data as string)
		  SerialOut.Text = SerialOut.Text + data + EndOfLine
		  SerialOut.VerticalScrollPosition=SerialOut.LineNumber(SerialOut.Text.Length)-2
		End Sub
	#tag EndMethod

	#tag Method, Flags = &h0
		Sub stopbuttonsetup(enabled as Boolean)
		  Var p As New Picture(StopButton.width, StopButton.height)
		  Var g As Graphics = p.Graphics
		  
		  if enabled then
		    g.DrawingColor = &cff0000
		  else
		    g.DrawingColor = &c999999
		  end if
		  g.FillOval(0, 0, g.Width, g.Height)
		  StopButton.Icon = p
		  StopButton.Enabled = enabled
		End Sub
	#tag EndMethod


	#tag Property, Flags = &h0
		footer_prop As string
	#tag EndProperty

	#tag Property, Flags = &h0
		forwarddelay_prop As string
	#tag EndProperty

	#tag Property, Flags = &h0
		header_prop As string
	#tag EndProperty

	#tag Property, Flags = &h0
		punchdelay_prop As string
	#tag EndProperty

	#tag Property, Flags = &h0
		tapefile As FolderItem
	#tag EndProperty


	#tag Constant, Name = nl, Type = String, Dynamic = False, Default = \"", Scope = Public
		#Tag Instance, Platform = Any, Language = Default, Definition  = \"&u0A"
	#tag EndConstant


#tag EndWindowCode

#tag Events DevicesPopupMenu
	#tag Event
		Sub SelectionChanged(item As DesktopMenuItem)
		  If Me.SelectedRowIndex = -1 Then
		    ConnectButton.Enabled = False
		  Else
		    ConnectButton.Enabled = True
		  End If
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events ConnectButton
	#tag Event
		Sub Pressed()
		  If Me.Caption = "Disconnect" Then // Disconnect from the serial device
		    PunchConnection.Close
		    Me.Caption = "Connect"
		    DevicesPopupMenu.Enabled = True
		    LookForSerialDevices.RunMode = Timer.RunModes.Multiple 'turn it on
		    PunchTools.Enabled = False
		    PunchTests.Enabled = False
		  Else // Connect to the serial device
		    // Set the serial device to the index of the one chosen in the popup menu
		    PunchConnection.Device = SerialDevice.At(DevicesPopupMenu.SelectedRowIndex)
		    Try
		      PunchConnection.Connect
		      DevicesPopupMenu.Enabled = False
		      LookForSerialDevices.RunMode = Timer.RunModes.Off
		      Me.Caption = "Disconnect"
		      PunchTools.Enabled = True
		      PunchTests.Enabled = True
		    Catch error As IOException
		      System.Beep
		      MessageBox("The selected serial device could not be opened.")
		    End Try
		  End If
		  
		  
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events LookForSerialDevices
	#tag Event
		Sub Action()
		  Var count As Integer = DevicesPopupMenu.RowCount
		  
		  If SerialDevice.Count <> count Then
		    // The number of serial devices has changed so update the menu
		    DevicesPopupMenu.RemoveAllRows
		    For i As Integer = 0 To SerialDevice.LastIndex
		      DevicesPopupMenu.AddRow(SerialDevice.At(i).Name)
		    Next
		    If SerialDevice.Count < count Then // a device has been removed
		      DevicesPopupMenu.SelectedRowIndex = 0
		    Else // one has been added so select the new device
		      DevicesPopupMenu.SelectedRowIndex = DevicesPopupMenu.LastRowIndex
		    End If
		  End If
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events PunchConnection
	#tag Event
		Sub DataReceived()
		  Var data As String
		  data = Me.LookAhead(Encodings.ASCII)
		  If data.IndexOf(EndOfLine.Windows) > -1 Then
		    //check if the thread is running
		    if sendTapeData.ThreadState = Thread.ThreadStates.Running then
		      sendTapeData.AddUserInterfaceUpdate("SerialData":Me.ReadAll(Encodings.ASCII))
		    else
		      SerialOut.Text = SerialOut.Text + Me.ReadAll(Encodings.ASCII) 
		      SerialOut.VerticalScrollPosition=SerialOut.LineNumber(SerialOut.Text.Length)-2
		    end if
		  End If
		  
		End Sub
	#tag EndEvent
	#tag Event
		Sub Error(e As RuntimeException)
		  System.Beep
		  MessageBox("An error occured while reading data from the device.")
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events LoadAndSendButton
	#tag Event
		Sub Pressed()
		  //open the tape
		  Var f As New FolderItem
		  f = FolderItem.ShowOpenFileDialog("")
		  
		  If f <> Nil Then
		    
		    tapefile = f
		    
		    if HeaderLabel.Value then
		      header_prop = header.text
		    else
		      header_prop = ""
		    end if
		    
		    if FooterLabel.value then
		      footer_prop = footer.text
		    else
		      footer_prop = ""
		    end if
		    
		    
		    forwarddelay_prop = ForwardDelay.text
		    punchdelay_prop = PunchDelay.text
		    
		    serialoutappend("Starting tape sending...")
		    sendTapeData.start
		    
		  End If
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events PunchDelayCB
	#tag Event
		Sub ValueChanged()
		  PunchDelay.Enabled = me.value
		  
		  if me.Value then
		    messagebox("Warning: These settings can damange the punch. Change with knowledge!")
		  end if
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events ForwardDelayCB
	#tag Event
		Sub ValueChanged()
		  ForwardDelay.Enabled = me.value
		  
		  if me.Value then
		    messagebox("Warning: These settings can damange the punch. Change with knowledge!")
		  end if
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events HeaderLabel
	#tag Event
		Sub ValueChanged()
		  header.Enabled = me.value
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events FooterLabel
	#tag Event
		Sub ValueChanged()
		  Footer.Enabled = me.value
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events StopButton
	#tag Event
		Sub Opening()
		  stopbuttonsetup(false)
		End Sub
	#tag EndEvent
	#tag Event
		Sub Pressed()
		  sendTapeData.Stop
		  PunchConnection.ClearBreak
		  stopbuttonsetup(false)
		  LoadAndSendButton.Enabled = true
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events Test1
	#tag Event
		Sub Pressed()
		  serialoutappend("Sending: **t1 (test1)")
		  PunchConnection.Write("**t1" +nl)
		  PunchConnection.Flush
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events Test2
	#tag Event
		Sub Pressed()
		  serialoutappend("Sending: **t2 (test2)")
		  PunchConnection.Write("**t2"+nl)
		  PunchConnection.Flush
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events Test3
	#tag Event
		Sub Pressed()
		  serialoutappend("Sending: **t3 (test3)")
		  PunchConnection.Write("**t3" + nl)
		  PunchConnection.Flush
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events Test4
	#tag Event
		Sub Pressed()
		  serialoutappend("Sending: **t4 (test4)")
		  PunchConnection.Write("**t4" + nl)
		  PunchConnection.Flush
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events TapeAdvance
	#tag Event
		Sub Pressed()
		  serialoutappend("Sending: **f1 (advance)")
		  PunchConnection.Write("**f1" + nl)
		  PunchConnection.Flush
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events TapeRetract
	#tag Event
		Sub Pressed()
		  serialoutappend("Sending: **b1 (retract)")
		  PunchConnection.Write("**b1" + nl)
		  PunchConnection.Flush
		End Sub
	#tag EndEvent
#tag EndEvents
#tag Events sendTapeData
	#tag Event
		Sub Run()
		  me.AddUserInterfaceUpdate("EnableStop":true)
		  me.AddUserInterfaceUpdate("EnableSend":false)
		  
		  //send the inital commands to the punch
		  
		  //punch delays
		  me.AddUserInterfaceUpdate("SerialData":"Setting Punch Delay: **p" + punchdelay_prop)
		  PunchConnection.Write("**p" + punchdelay_prop + nl)
		  PunchConnection.Flush
		  me.YieldToNext
		  
		  //forward delay
		  me.AddUserInterfaceUpdate("SerialData":"Setting Forward Delay: **d" + forwarddelay_prop)
		  PunchConnection.Write("**d" + forwarddelay_prop + nl)
		  PunchConnection.Flush
		  me.YieldToNext
		  
		  //test all pins
		  me.AddUserInterfaceUpdate("SerialData":"Testing All Pins: **t4")
		  PunchConnection.Write("**t4" + nl)
		  PunchConnection.Flush
		  me.YieldToNext
		  
		  dim tapeadvance as Double = header_prop.ToDouble
		  dim tapeadvance_int as integer
		  
		  //advance the tape
		  if header_prop <> "" then
		    //convert to advance units
		    tapeadvance = tapeadvance * 0.3125
		    tapeadvance_int = tapeadvance
		    me.AddUserInterfaceUpdate("SerialData":"Advancing Tape: **f" + tapeadvance_int.ToString)
		    PunchConnection.Write("**f" + tapeadvance_int.ToString + nl)
		    PunchConnection.Flush
		    me.YieldToNext
		  end if
		  
		  //punch the lines in the file
		  dim t as TextInputStream = TextInputStream.Open(tapefile)
		  dim line as string
		  while not t.eof
		    line = t.ReadLine + EndOfLine
		    me.AddUserInterfaceUpdate("SerialData":line)
		    PunchConnection.Write(line)
		    PunchConnection.Flush
		    me.YieldToNext
		  wend
		  
		  if footer_prop <> "" then
		    //advance the tape
		    tapeadvance = footer_prop.ToDouble
		    //convert to advance units
		    tapeadvance = tapeadvance * 0.3125
		    tapeadvance_int = tapeadvance
		    me.AddUserInterfaceUpdate("SerialData":"Advancing Tape: **f" + tapeadvance_int.ToString)
		    PunchConnection.Write("**f" + tapeadvance_int.ToString + nl)
		    PunchConnection.Flush
		    me.YieldToNext
		  end if
		  
		  //test all pins
		  me.AddUserInterfaceUpdate("SerialData":"Testing All Pins: **t4")
		  PunchConnection.Write("**t4" + nl)
		  PunchConnection.Flush
		  me.YieldToNext
		  
		  //eject the tape
		  me.AddUserInterfaceUpdate("SerialData":"Ejecting Tape: **f60")
		  PunchConnection.Write("**f60" + nl)
		  PunchConnection.Flush
		  me.YieldToNext
		  
		  me.AddUserInterfaceUpdate("EnableSend": true)
		  me.AddUserInterfaceUpdate("EnableStop": false)
		End Sub
	#tag EndEvent
	#tag Event
		Sub UserInterfaceUpdate(data() as Dictionary)
		  For Each update As Dictionary In data
		    If update.HasKey("SerialData") Then
		      //serialoutappend(update.Value("SerialData").StringValue)
		      SerialOut.Text = SerialOut.Text + update.Value("SerialData").StringValue + EndOfLine
		      SerialOut.VerticalScrollPosition=SerialOut.LineNumber(SerialOut.Text.Length)-2
		    elseif update.HasKey("EnableSend") then
		      LoadAndSendButton.Enabled = update.value("EnableSend").BooleanValue
		    elseif update.HasKey("EnableStop") then
		      stopbuttonsetup(update.value("EnableStop").BooleanValue)
		    End If
		  Next
		  
		  me.YieldToNext
		End Sub
	#tag EndEvent
#tag EndEvents
#tag ViewBehavior
	#tag ViewProperty
		Name="Name"
		Visible=true
		Group="ID"
		InitialValue=""
		Type="String"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="Interfaces"
		Visible=true
		Group="ID"
		InitialValue=""
		Type="String"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="Super"
		Visible=true
		Group="ID"
		InitialValue=""
		Type="String"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="Width"
		Visible=true
		Group="Size"
		InitialValue="600"
		Type="Integer"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="Height"
		Visible=true
		Group="Size"
		InitialValue="400"
		Type="Integer"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="MinimumWidth"
		Visible=true
		Group="Size"
		InitialValue="64"
		Type="Integer"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="MinimumHeight"
		Visible=true
		Group="Size"
		InitialValue="64"
		Type="Integer"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="MaximumWidth"
		Visible=true
		Group="Size"
		InitialValue="32000"
		Type="Integer"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="MaximumHeight"
		Visible=true
		Group="Size"
		InitialValue="32000"
		Type="Integer"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="Type"
		Visible=true
		Group="Frame"
		InitialValue="0"
		Type="Types"
		EditorType="Enum"
		#tag EnumValues
			"0 - Document"
			"1 - Movable Modal"
			"2 - Modal Dialog"
			"3 - Floating Window"
			"4 - Plain Box"
			"5 - Shadowed Box"
			"6 - Rounded Window"
			"7 - Global Floating Window"
			"8 - Sheet Window"
			"9 - Metal Window"
			"11 - Modeless Dialog"
		#tag EndEnumValues
	#tag EndViewProperty
	#tag ViewProperty
		Name="Title"
		Visible=true
		Group="Frame"
		InitialValue="Untitled"
		Type="String"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="HasCloseButton"
		Visible=true
		Group="Frame"
		InitialValue="True"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="HasMaximizeButton"
		Visible=true
		Group="Frame"
		InitialValue="True"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="HasMinimizeButton"
		Visible=true
		Group="Frame"
		InitialValue="True"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="HasFullScreenButton"
		Visible=true
		Group="Frame"
		InitialValue="False"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="Resizeable"
		Visible=true
		Group="Frame"
		InitialValue="True"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="Composite"
		Visible=false
		Group="OS X (Carbon)"
		InitialValue="False"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="MacProcID"
		Visible=false
		Group="OS X (Carbon)"
		InitialValue="0"
		Type="Integer"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="FullScreen"
		Visible=false
		Group="Behavior"
		InitialValue="False"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="DefaultLocation"
		Visible=true
		Group="Behavior"
		InitialValue="2"
		Type="Locations"
		EditorType="Enum"
		#tag EnumValues
			"0 - Default"
			"1 - Parent Window"
			"2 - Main Screen"
			"3 - Parent Window Screen"
			"4 - Stagger"
		#tag EndEnumValues
	#tag EndViewProperty
	#tag ViewProperty
		Name="Visible"
		Visible=true
		Group="Behavior"
		InitialValue="True"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="ImplicitInstance"
		Visible=true
		Group="Windows Behavior"
		InitialValue="True"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="HasBackgroundColor"
		Visible=true
		Group="Background"
		InitialValue="False"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="BackgroundColor"
		Visible=true
		Group="Background"
		InitialValue="&cFFFFFF"
		Type="ColorGroup"
		EditorType="ColorGroup"
	#tag EndViewProperty
	#tag ViewProperty
		Name="Backdrop"
		Visible=true
		Group="Background"
		InitialValue=""
		Type="Picture"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="MenuBar"
		Visible=true
		Group="Menus"
		InitialValue=""
		Type="DesktopMenuBar"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="MenuBarVisible"
		Visible=true
		Group="Deprecated"
		InitialValue="False"
		Type="Boolean"
		EditorType=""
	#tag EndViewProperty
	#tag ViewProperty
		Name="tapefile"
		Visible=false
		Group="Behavior"
		InitialValue=""
		Type="Integer"
		EditorType=""
	#tag EndViewProperty
#tag EndViewBehavior
