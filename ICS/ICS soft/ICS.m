function varargout = ICS(varargin)
% ICS M-file for ICS.fig
%      ICS, by itself, creates a new ICS or raises the existing
%      singleton*.
%
%      H = ICS returns the handle to a new ICS or the handle to
%      the existing singleton*.
%
%      ICS('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in ICS.M with the given input arguments.
%
%      ICS('Property','Value',...) creates a new ICS or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ICS_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to ICS_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ICS

% Last Modified by GUIDE v2.5 19-Jun-2012 15:44:43

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @ICS_OpeningFcn, ...
                   'gui_OutputFcn',  @ICS_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before ICS is made visible.
function ICS_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to ICS (see VARARGIN)

% Choose default command line output for ICS
handles.output = hObject;

handles.xdimension = 512;
handles.ydimension = 512;
handles.redcheckbox = 0;
handles.greencheckbox = 0;
handles.bluecheckbox = 0;
handles.rednumber = 0;
handles.greennumber = 0;
handles.bluenumber = 0;
handles.beamradius = 10;
handles.Nrg = 0;
handles.Nrgb = 0;
handles.Nrb = 0;
handles.Ngb = 0;
handles.Xi1 = 0;
handles.Xi2 = 0;
handles.Xi3 = 0;
handles.Xi4 = 0;
handles.Xi5 = 0;
handles.Xi6 = 0;
handles.brightnessred = 1;
handles.brightnessgreen = 1;
handles.brightnessblue = 1;
handles.bcgrndred = 0;
handles.bcgrndgreen = 0;
handles.bcgrndblue = 0;
handles.g0 = 1;
handles.w = 10;
handles.ginf = 0;
handles.range = 20;
handles.niter = 100;
handles.optimstop = false;
handles.filename = [];


set(gcf,'CurrentAxes',handles.rgb)
image(imread('logoMax.jpg'));
axis off

set(gcf,'CurrentAxes',handles.b)
image(imread('logoMaxB.jpg'));
axis off


set(gcf,'CurrentAxes',handles.g)
image(imread('logoMaxG.jpg'));
axis off

set(gcf,'CurrentAxes',handles.r)
image(imread('logoMaxR.jpg'));
axis off


% Update handles structure
guidata(hObject, handles);

% UIWAIT makes ICS wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = ICS_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function xdimension_Callback(hObject, eventdata, handles)
% hObject    handle to xdimension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of xdimension as text
%        str2double(get(hObject,'String')) returns contents of xdimension as a double

xdimension = str2double(get(hObject,'string'));

            if isnan(xdimension)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end

    handles.xdimension = xdimension;

    guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function xdimension_CreateFcn(hObject, eventdata, handles)
% hObject    handle to xdimension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ydimension_Callback(hObject, eventdata, handles)
% hObject    handle to ydimension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ydimension as text
%        str2double(get(hObject,'String')) returns contents of ydimension as a double

ydimension = str2double(get(hObject,'string'));

            if isnan(ydimension)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end

    handles.ydimension = ydimension;

    guidata(hObject,handles);





% --- Executes during object creation, after setting all properties.
function ydimension_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ydimension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function beamradius_Callback(hObject, eventdata, handles)
% hObject    handle to beamradius (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of beamradius as text
%        str2double(get(hObject,'String')) returns contents of beamradius as a double

 beamradius = str2double(get(hObject,'string'));

            if isnan(beamradius)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end

    handles.beamradius = beamradius;

    guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function beamradius_CreateFcn(hObject, eventdata, handles)
% hObject    handle to beamradius (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in bluecheckbox.
function bluecheckbox_Callback(hObject, eventdata, handles)
% hObject    handle to bluecheckbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of bluecheckbox

if (get(hObject,'Value') == get(hObject,'Max'))
        handles.bluecheckbox = 1;
    else
        handles.bluecheckbox = 0;
    end

    guidata(hObject,handles);



% --- Executes on button press in greencheckbox.
function greencheckbox_Callback(hObject, eventdata, handles)
% hObject    handle to greencheckbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of greencheckbox

if (get(hObject,'Value') == get(hObject,'Max'))
        handles.greencheckbox = 1;
    else
        handles.greencheckbox = 0;
    end

    guidata(hObject,handles);


% --- Executes on button press in redcheckbox.
function redcheckbox_Callback(hObject, eventdata, handles)
% hObject    handle to redcheckbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of redcheckbox

if (get(hObject,'Value') == get(hObject,'Max'))
        handles.redcheckbox = 1;
    else
        handles.redcheckbox = 0;
    end

    guidata(hObject,handles);
    
    
    

function brightnessblue_Callback(hObject, eventdata, handles)
% hObject    handle to brightnessblue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of brightnessblue as text
%        str2double(get(hObject,'String')) returns contents of brightnessblue as a double

brightnessblue = str2double(get(hObject,'string'));

            if isnan(brightnessblue)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if brightnessblue > 1
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end
            
            if brightnessblue < 0
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end

    handles.brightnessblue = brightnessblue;

    guidata(hObject,handles);


    
    


% --- Executes during object creation, after setting all properties.
function brightnessblue_CreateFcn(hObject, eventdata, handles)
% hObject    handle to brightnessblue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function brightnessgreen_Callback(hObject, eventdata, handles)
% hObject    handle to brightnessgreen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of brightnessgreen as text
%        str2double(get(hObject,'String')) returns contents of brightnessgreen as a double

 brightnessgreen = str2double(get(hObject,'string'));

            if isnan(brightnessgreen)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if brightnessgreen > 1
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end
            
            if brightnessgreen < 0
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end

    handles.brightnessgreen = brightnessgreen;

    guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function brightnessgreen_CreateFcn(hObject, eventdata, handles)
% hObject    handle to brightnessgreen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function brightnessred_Callback(hObject, eventdata, handles)
% hObject    handle to brightnessred (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of brightnessred as text
%        str2double(get(hObject,'String')) returns contents of brightnessred as a double


  brightnessred = str2double(get(hObject,'string'));

            if isnan(brightnessred)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if brightnessred > 1
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end
            
            if brightnessred < 0
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end

    handles.brightnessred = brightnessred;

    guidata(hObject,handles);





% --- Executes during object creation, after setting all properties.
function brightnessred_CreateFcn(hObject, eventdata, handles)
% hObject    handle to brightnessred (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function bcgrndred_Callback(hObject, eventdata, handles)
% hObject    handle to bcgrndred (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bcgrndred as text
%        str2double(get(hObject,'String')) returns contents of bcgrndred as a double


   bcgrndred = str2double(get(hObject,'string'));

            if isnan(bcgrndred)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if bcgrndred > 1
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end
            
            if bcgrndred < 0
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end

    handles.bcgrndred = bcgrndred;

    guidata(hObject,handles);






% --- Executes during object creation, after setting all properties.
function bcgrndred_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bcgrndred (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function bcgrndgreen_Callback(hObject, eventdata, handles)
% hObject    handle to bcgrndgreen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bcgrndgreen as text
%        str2double(get(hObject,'String')) returns contents of bcgrndgreen as a double

bcgrndgreen = str2double(get(hObject,'string'));

            if isnan(bcgrndgreen)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if bcgrndgreen > 1
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end
            
            if bcgrndgreen < 0
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end

    handles.bcgrndgreen = bcgrndgreen;

    guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function bcgrndgreen_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bcgrndgreen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function bcgrndblue_Callback(hObject, eventdata, handles)
% hObject    handle to bcgrndblue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bcgrndblue as text
%        str2double(get(hObject,'String')) returns contents of bcgrndblue as a double

bcgrndblue = str2double(get(hObject,'string'));

            if isnan(bcgrndblue)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if bcgrndblue > 1
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end
            
            if bcgrndblue < 0
                errordlg('Value of brightness should be between 0 and 1','Bad Input','modal')
            end

    handles.bcgrndblue = bcgrndblue;

    guidata(hObject,handles);
    



% --- Executes during object creation, after setting all properties.
function bcgrndblue_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bcgrndblue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function bluenumber_Callback(hObject, eventdata, handles)
% hObject    handle to bluenumber (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of bluenumber as text
%        str2double(get(hObject,'String')) returns contents of bluenumber as a double

 bluenumber = str2double(get(hObject,'string'));

            if isnan(bluenumber)
                errordlg('You must enter a numeric value','Bad Input','modal')
            end

    handles.bluenumber = bluenumber;
    numblue = round((handles.bluenumber*pi*(handles.beamradius^2))/(handles.xdimension*handles.ydimension)*100)/100;
    set(handles.numblue, 'String', numblue);
    curbluenumber = bluenumber - handles.Nrb - handles.Ngb - handles.Nrgb;
    set(handles.Nb, 'String', curbluenumber);
    
                set(handles.Ngcur, 'String', ' ');
                set(handles.Nrcur, 'String', ' ');
                set(handles.Nbcur, 'String', ' ');
                set(handles.Nrbcur, 'String', ' ');
                set(handles.Nrgcur, 'String', ' ');
                set(handles.Ngbcur, 'String', ' ');
                set(handles.Nrgbcur, 'String', ' ');
    
    
    
    guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function bluenumber_CreateFcn(hObject, eventdata, handles)
% hObject    handle to bluenumber (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function greennumber_Callback(hObject, eventdata, handles)
% hObject    handle to greennumber (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of greennumber as text
%        str2double(get(hObject,'String')) returns contents of greennumber as a double

greennumber = str2double(get(hObject,'string'));

            if isnan(greennumber)
                errordlg('You must enter a numeric value','Bad Input','modal')
            end

    handles.greennumber = greennumber;
    numgreen = round((handles.greennumber*pi*(handles.beamradius^2))/(handles.xdimension*handles.ydimension)*100)/100;
    set(handles.numgreen, 'String', numgreen);
    curgreennumber = greennumber - handles.Nrg - handles.Ngb - handles.Nrgb;
    set(handles.Ng, 'String', curgreennumber);
    
    set(handles.Ngcur, 'String', ' ');
                set(handles.Nrcur, 'String', ' ');
                set(handles.Nbcur, 'String', ' ');
                set(handles.Nrbcur, 'String', ' ');
                set(handles.Nrgcur, 'String', ' ');
                set(handles.Ngbcur, 'String', ' ');
                set(handles.Nrgbcur, 'String', ' ');
    
    
    
    
    guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function greennumber_CreateFcn(hObject, eventdata, handles)
% hObject    handle to greennumber (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function rednumber_Callback(hObject, eventdata, handles)
% hObject    handle to rednumber (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of rednumber as text
%        str2double(get(hObject,'String')) returns contents of rednumber as a double


rednumber = str2double(get(hObject,'string'));

            if isnan(rednumber)
                errordlg('You must enter a numeric value','Bad Input','modal')
            end

    handles.rednumber = rednumber;
    numred = round((handles.rednumber*pi*(handles.beamradius^2))/(handles.xdimension*handles.ydimension)*100)/100;
    set(handles.numred, 'String', numred);
    currednumber = rednumber - handles.Nrg - handles.Nrb - handles.Nrgb;
    set(handles.Nr, 'String', currednumber);
    
    set(handles.Ngcur, 'String', ' ');
                set(handles.Nrcur, 'String', ' ');
                set(handles.Nbcur, 'String', ' ');
                set(handles.Nrbcur, 'String', ' ');
                set(handles.Nrgcur, 'String', ' ');
                set(handles.Ngbcur, 'String', ' ');
                set(handles.Nrgbcur, 'String', ' ');
    
    
    
    
    guidata(hObject,handles);


    guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function rednumber_CreateFcn(hObject, eventdata, handles)
% hObject    handle to rednumber (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Nrg_Callback(hObject, eventdata, handles)
% hObject    handle to Nrg (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Nrg as text
%        str2double(get(hObject,'String')) returns contents of Nrg as a double

 Nrg = str2double(get(hObject,'string'));

                       
            if isnan(Nrg)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            
            if Nrg > (handles.rednumber - handles.Nrb - handles.Xi1 - handles.Xi2 - handles.Xi4 - handles.Xi5 - handles.Xi6 - handles.Nrgb) | Nrg > (handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi4 - handles.Xi5 - handles.Xi6 - handles.Ngb - handles.Nrgb)
                errordlg('Value of Nrg cannot exceed the total number of red or green species','Bad Input','modal')
                set(handles.Nr, 'String', 'Err');
                set(handles.Ng, 'String', 'Err');
                set(handles.Nb, 'String', 'Err');
                
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
                
            else
                currrednumber = handles.rednumber - handles.Nrb - handles.Nrgb - Nrg;
                curgreennumber = handles.greennumber - handles.Ngb - handles.Nrgb - Nrg;
                curbluenumber = handles.bluenumber - handles.Nrb - handles.Ngb - handles.Nrgb;
                set(handles.Nr, 'String', currrednumber);
                set(handles.Ng, 'String', curgreennumber);
                set(handles.Nb, 'String', curbluenumber);
                             
                
                handles.Nrg = Nrg;
                
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                                
            end
                        
         
            
    guidata(hObject,handles);






% --- Executes during object creation, after setting all properties.
function Nrg_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Nrg (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Nrb_Callback(hObject, eventdata, handles)
% hObject    handle to Nrb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Nrb as text
%        str2double(get(hObject,'String')) returns contents of Nrb as a double

 Nrb = str2double(get(hObject,'string'));

                       
            if isnan(Nrb)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            
            
            if Nrb > (handles.rednumber - handles.Nrg - handles.Nrgb - handles.Xi1 - handles.Xi2 - handles.Xi4 - handles.Xi5 - handles.Xi6) | Nrb > (handles.bluenumber - handles.Ngb - handles.Nrgb - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Xi5 - handles.Xi6)
                errordlg('Value of Nrb cannot exceed the total number of red or blue species','Bad Input','modal')
                set(handles.Nr, 'String', 'Err');
                set(handles.Nb, 'String', 'Err');
                set(handles.Ng, 'String', 'Err');
                
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
                
            else
                currrednumber = handles.rednumber - handles.Nrg - handles.Nrgb - Nrb;
                curgreennumber = handles.greennumber - handles.Ngb - handles.Nrgb - handles.Nrg;
                curbluenumber = handles.bluenumber - handles.Ngb - handles.Nrgb - Nrb;
                set(handles.Nr, 'String', currrednumber);
                set(handles.Ng, 'String', curgreennumber);
                set(handles.Nb, 'String', curbluenumber);
                handles.Nrb = Nrb;
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
                
                
            end
                        
                      
            
    guidata(hObject,handles);






% --- Executes during object creation, after setting all properties.
function Nrb_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Nrb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Ngb_Callback(hObject, eventdata, handles)
% hObject    handle to Ngb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Ngb as text
%        str2double(get(hObject,'String')) returns contents of Ngb as a double

   Ngb = str2double(get(hObject,'string'));

                       
            if isnan(Ngb)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if Ngb > (handles.greennumber - handles.Nrg - handles.Nrgb - handles.Xi1 - handles.Xi3 - handles.Xi4 - handles.Xi5 - handles.Xi6) | Ngb > (handles.bluenumber - handles.Nrb - handles.Nrgb - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Xi5 - handles.Xi6)
                errordlg('Value of Ngb cannot exceed the total number of green or blue species','Bad Input','modal')
                set(handles.Ng, 'String', 'Err');
                set(handles.Nb, 'String', 'Err');
                set(handles.Nr, 'String', 'Err');
                
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
                
            else
                currrednumber = handles.rednumber - handles.Nrb - handles.Nrgb - handles.Nrg;
                curgreennumber = handles.greennumber - handles.Nrg - handles.Nrgb - Ngb;
                curbluenumber = handles.bluenumber - handles.Nrb - handles.Nrgb - Ngb;
                set(handles.Nr, 'String', currrednumber);
                set(handles.Ng, 'String', curgreennumber);
                set(handles.Nb, 'String', curbluenumber);
                handles.Ngb = Ngb;
                
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
                
            end
                        
      
            
    guidata(hObject,handles);
    



% --- Executes during object creation, after setting all properties.
function Ngb_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Ngb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Nrgb_Callback(hObject, eventdata, handles)
% hObject    handle to Nrgb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Nrgb as text
%        str2double(get(hObject,'String')) returns contents of Nrgb as a double

 Nrgb = str2double(get(hObject,'string'));
 
 
            if isnan(Nrgb)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
                curRd = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrg;
                curGrn = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Ngb;
                curBl = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb;
                curRdG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRdB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGrB = handles.Ngb + handles.Xi3 - handles.Xi6;
                
               
              
                
            
            if Nrgb > curRd | Nrgb > curGrn | Nrgb > curBl | Nrgb > curRdG | Nrgb > curGrB | Nrgb > curRdB
                errordlg('Value of Nrgb cannot exceed the total number of red or green or blue species','Bad Input','modal')
                set(handles.Nr, 'String', 'Err');
                set(handles.Ng, 'String', 'Err');
                set(handles.Nb, 'String', 'Err');
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
            else
                currrednumber = handles.rednumber - handles.Nrb - handles.Nrg - Nrgb;
                curgreennumber = handles.greennumber - handles.Ngb - handles.Nrg - Nrgb;
                curbluenumber = handles.bluenumber - handles.Ngb - handles.Nrb - Nrgb;
                set(handles.Nr, 'String', currrednumber);
                set(handles.Ng, 'String', curgreennumber);
                set(handles.Nb, 'String', curbluenumber);
                handles.Nrgb = Nrgb;
                
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
                
                
            end
               
                   
           
    guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function Nrgb_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Nrgb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Xi1_Callback(hObject, eventdata, handles)
% hObject    handle to Xi1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Xi1 as text
%        str2double(get(hObject,'String')) returns contents of Xi1 as a double

Xi1 = str2double(get(hObject,'string'));

                       
            if isnan(Xi1)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if Xi1 > (handles.greennumber - handles.Nrg - handles.Nrgb - handles.Ngb) | Xi1 > (handles.rednumber - handles.Nrb - handles.Nrgb - handles.Nrg)
                errordlg('Value of Xi1 cannot exceed the number of non-colocolized red or green species','Bad Input','modal')
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
                
            else
                
                handles.Xi1 = Xi1;
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
                
                
            end
                        
      
            
    handles.Xi1 = Xi1;
    guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function Xi1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Xi1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Xi2_Callback(hObject, eventdata, handles)
% hObject    handle to Xi2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Xi2 as text
%        str2double(get(hObject,'String')) returns contents of Xi2 as a double


Xi2 = str2double(get(hObject,'string'));

                       
            if isnan(Xi2)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if Xi2 > (handles.bluenumber - handles.Nrb - handles.Nrgb - handles.Ngb) | Xi2 > (handles.rednumber - handles.Nrb - handles.Nrgb - handles.Nrg)
                errordlg('Value of Xi2 cannot exceed the number of non-colocolized red or blue species','Bad Input','modal')
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
                
            else
                handles.Xi2 = Xi2;
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
                
            end
                        
      
            
    
    guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function Xi2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Xi2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Xi3_Callback(hObject, eventdata, handles)
% hObject    handle to Xi3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Xi3 as text
%        str2double(get(hObject,'String')) returns contents of Xi3 as a double

Xi3 = str2double(get(hObject,'string'));

                       
            if isnan(Xi3)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if Xi3 > (handles.greennumber - handles.Nrg - handles.Nrgb - handles.Ngb) | Xi3 > (handles.bluenumber - handles.Nrb - handles.Nrgb - handles.Ngb)
                errordlg('Value of Xi3 cannot exceed the number of non-colocolized green or blue species','Bad Input','modal')
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
            else
                handles.Xi3 = Xi3;
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
               
            end
                        
      
            
    handles.Xi3 = Xi3;
    guidata(hObject,handles);
    

% --- Executes during object creation, after setting all properties.
function Xi3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Xi3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Xi4_Callback(hObject, eventdata, handles)
% hObject    handle to Xi4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Xi4 as text
%        str2double(get(hObject,'String')) returns contents of Xi4 as a double

Xi4 = str2double(get(hObject,'string'));


Bluenc = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Nrb - handles.Ngb - handles.Nrgb;


                       
            if isnan(Xi4)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if Xi4 > Bluenc | Xi4 > (handles.Nrg + handles.Xi1)
                errordlg('Value of Xi4 cannot exceed the number of non-colocolized blue species or colocolized red and green species','Bad Input','modal')
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
            else
                
                   handles.Xi4 = Xi4;
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
            end
                        
      
            
    
    guidata(hObject,handles);
    
    

% --- Executes during object creation, after setting all properties.
function Xi4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Xi4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Xi5_Callback(hObject, eventdata, handles)
% hObject    handle to Xi5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Xi5 as text
%        str2double(get(hObject,'String')) returns contents of Xi5 as a double


Xi5 = str2double(get(hObject,'string'));

             Greennc = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Nrg - handles.Ngb - handles.Nrgb;          
            if isnan(Xi5)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if Xi5 > Greennc | Xi5 > (handles.Nrb + handles.Xi2)
                errordlg('Value of Xi5 cannot exceed the number of non-colocolized green species or colocolized red and blue species','Bad Input','modal')
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
            else
                
                   handles.Xi5 = Xi5;
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
            end
                        
      
            
    
    guidata(hObject,handles);
    
    

% --- Executes during object creation, after setting all properties.
function Xi5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Xi5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Xi6_Callback(hObject, eventdata, handles)
% hObject    handle to Xi6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Xi6 as text
%        str2double(get(hObject,'String')) returns contents of Xi6 as a double


Xi6 = str2double(get(hObject,'string'));

             Rednc = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Nrg - handles.Nrb - handles.Nrgb;          
            if isnan(Xi6)
                errordlg('You must enter a positive integer','Bad Input','modal')
            end
            
            if Xi6 > Rednc | Xi6 > (handles.Ngb + handles.Xi3)
                errordlg('Value of Xi6 cannot exceed the number of non-colocolized red species or colocolized green and blue species','Bad Input','modal')
                set(handles.Ngcur, 'String', 'Err');
                set(handles.Nrcur, 'String', 'Err');
                set(handles.Nbcur, 'String', 'Err');
                set(handles.Nrbcur, 'String', 'Err');
                set(handles.Nrgcur, 'String', 'Err');
                set(handles.Ngbcur, 'String', 'Err');
                set(handles.Nrgbcur, 'String', 'Err');
            else
                
                   handles.Xi6 = Xi6;
                curRed = handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg;
                curGreen = handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb;
                curBlue = handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb;
                curRG = handles.Nrg + handles.Xi1 - handles.Xi4;
                curRB = handles.Nrb + handles.Xi2 - handles.Xi5;
                curGB = handles.Ngb + handles.Xi3 - handles.Xi6;
                curRGB = handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6;
                set(handles.Ngcur, 'String', curGreen);
                set(handles.Nrcur, 'String', curRed);
                set(handles.Nbcur, 'String', curBlue);
                set(handles.Nrbcur, 'String', curRB);
                set(handles.Nrgcur, 'String', curRG);
                set(handles.Ngbcur, 'String', curGB);
                set(handles.Nrgbcur, 'String', curRGB);
                
            end
                        
      
            
    
    guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function Xi6_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Xi6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes on button press in imagegen.
function imagegen_Callback(hObject, eventdata, handles)
% hObject    handle to imagegen (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


if handles.redcheckbox == 0 & handles.greencheckbox == 0 & handles.bluecheckbox == 0 %checking if the channel is active

    errordlg('Make sure at least one channel is checked','Bad Input','modal')
    
end

if handles.redcheckbox == 1 & handles.greencheckbox == 0 & handles.bluecheckbox == 0 %checking if the channel is active
    
    
    Ntotalred = poissrnd(handles.rednumber);
      
    set(handles.Nr, 'String', ' ');
    set(handles.Nb, 'String', ' ');
    set(handles.Ng, 'String', ' ');
    set(handles.Nrcur, 'String', handles.rednumber);
    set(handles.Nbcur, 'String', ' ');
    set(handles.Ngcur, 'String', ' ');
    set(handles.Nrbcur, 'String', ' ');
    set(handles.Nrgcur, 'String', ' ');
    set(handles.Ngbcur, 'String', ' ');
    set(handles.Nrgbcur, 'String', ' ');
   
    set(handles.NrP, 'String', Ntotalred);
    set(handles.NgP, 'String', ' ');
    set(handles.NbP, 'String', ' ');
    set(handles.NrbP, 'String', ' ');
    set(handles.NrgP, 'String', ' ');
    set(handles.NgbP, 'String', ' ');
    set(handles.NrgbP, 'String', ' ');
    
    
    RGB = zeros(handles.xdimension, handles.ydimension, 3);

    X = ceil((handles.xdimension).*rand(Ntotalred, 1));
    Y = ceil((handles.ydimension).*rand(Ntotalred, 1));

    % X and Y are arrays of random integers. rand(Ntotalred,1) generates a matrix
    % of random numbers from 0 to 1 with the dimensions Ntotalred x 1. Multiplication
    % by (handles.x(y)dimension + 64) scales this array to the size of the image matrix. ceil rounds
    % the numbers in the array to the nearest greater integer.
   

    
    %The intensity at the detector depends on the position of a fluorophore
    %(fluorophores) inside the beam that has Gaussian profile. In the following
    %cycle Gaussian values are calculated for the matrix elements where the
    %molecules were placed by the random number generator. Then these Gaussian
    % values are multiplied by the value of brightness and summed up to create
    % a value of intensity originating from one pixel. This value is written
    % into the matrix Pixel. The lenght of the vector Pixel is k*k. i.e. the
    % total number of pixels in the image.

    

    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:Ntotalred
            
                x = i - X(l);
                y = j - Y(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessred;
                
            end     
        
        RGB(i, j, 1) = sum(pixint);
       
        end
    end
    
    
   
    
    

    emptymatrix = zeros(handles.xdimension, handles.ydimension);
    
        set(gcf,'CurrentAxes',handles.rgb);
        Red = cat(3, RGB(:, :, 1), emptymatrix, emptymatrix);
        imwrite(Red, 'Redtemp.bmp');
        imwrite(Red, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.b)
        image(imread('logoMaxB.jpg'));
        axis off


        set(gcf,'CurrentAxes',handles.g)
        image(imread('logoMaxG.jpg'));
        axis off
        
        
           
        set(gcf,'CurrentAxes',handles.r);
        image(imread ('Redtemp.bmp'));
        axis off;
 
        
        handles.filename = 'RGBtemp';
        guidata(hObject,handles);
        
        
end


if handles.redcheckbox == 0 & handles.greencheckbox == 1 & handles.bluecheckbox == 0 %checking if the channel is active
    
    
    Ntotalgreen = poissrnd(handles.greennumber);
      
    set(handles.Nr, 'String', ' ');
    set(handles.Nb, 'String', ' ');
    set(handles.Ng, 'String', ' ');
    set(handles.Nrcur, 'String', ' ');
    set(handles.Nbcur, 'String', ' ');
    set(handles.Ngcur, 'String', handles.greennumber);
    set(handles.Nrbcur, 'String', ' ');
    set(handles.Nrgcur, 'String', ' ');
    set(handles.Ngbcur, 'String', ' ');
    set(handles.Nrgbcur, 'String', ' ');
   
    set(handles.NrP, 'String', ' ');
    set(handles.NgP, 'String', Ntotalgreen);
    set(handles.NbP, 'String', ' ');
    set(handles.NrbP, 'String', ' ');
    set(handles.NrgP, 'String', ' ');
    set(handles.NgbP, 'String', ' ');
    set(handles.NrgbP, 'String', ' ');
   
    
    
    RGB = zeros(handles.xdimension, handles.ydimension, 3);

    X = ceil((handles.xdimension).*rand(Ntotalgreen, 1));
    Y = ceil((handles.ydimension).*rand(Ntotalgreen, 1));

  
    

    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:Ntotalgreen
            
                x = i - X(l);
                y = j - Y(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessgreen;
                
            end     
        
        RGB(i, j, 2) = sum(pixint);
       
        end
    end
    
    
   
    
    

    emptymatrix = zeros(handles.xdimension, handles.ydimension);
    
        set(gcf,'CurrentAxes',handles.rgb);
        Green = cat(3, emptymatrix, RGB(:, :, 2), emptymatrix);
        imwrite(Green, 'Greentemp.bmp');
        imwrite(Green, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.b)
        image(imread('logoMaxB.jpg'));
        axis off


        set(gcf,'CurrentAxes',handles.r)
        image(imread('logoMaxR.jpg'));
        axis off
        
        
           
        set(gcf,'CurrentAxes',handles.g);
        image(imread ('Greentemp.bmp'));
        axis off;
        
        
        handles.filename = 'RGBtemp';
        guidata(hObject,handles);
 

end

if handles.redcheckbox == 0 & handles.greencheckbox == 0 & handles.bluecheckbox == 1 %checking if the channel is active
    
    
    Ntotalblue = poissrnd(handles.bluenumber);
      
    set(handles.Nr, 'String', ' ');
    set(handles.Nb, 'String', ' ');
    set(handles.Ng, 'String', ' ');
    set(handles.Nrcur, 'String', ' ');
    set(handles.Nbcur, 'String', handles.bluenumber);
    set(handles.Ngcur, 'String', ' ');
    set(handles.Nrbcur, 'String', ' ');
    set(handles.Nrgcur, 'String', ' ');
    set(handles.Ngbcur, 'String', ' ');
    set(handles.Nrgbcur, 'String', ' ');
   
    set(handles.NrP, 'String', ' ');
    set(handles.NgP, 'String', ' ');
    set(handles.NbP, 'String', Ntotalblue);
    set(handles.NrbP, 'String', ' ');
    set(handles.NrgP, 'String', ' ');
    set(handles.NgbP, 'String', ' ');
    set(handles.NrgbP, 'String', ' ');
   
    
    
    
    RGB = zeros(handles.xdimension, handles.ydimension, 3);

    X = ceil((handles.xdimension).*rand(Ntotalblue, 1));
    Y = ceil((handles.ydimension).*rand(Ntotalblue, 1));

  
    

    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:Ntotalblue
            
                x = i - X(l);
                y = j - Y(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessblue;
                
            end     
        
        RGB(i, j, 3) = sum(pixint);
       
        end
    end
    
    
   
    
    

    emptymatrix = zeros(handles.xdimension, handles.ydimension);
    
        set(gcf,'CurrentAxes',handles.rgb);
        Blue = cat(3, emptymatrix, emptymatrix, RGB(:, :, 3));
        imwrite(Blue, 'RGBtemp.bmp');
        imwrite(Blue, 'Bluetemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.r)
        image(imread('logoMaxR.jpg'));
        axis off


        set(gcf,'CurrentAxes',handles.g)
        image(imread('logoMaxG.jpg'));
        axis off
        
        
           
        set(gcf,'CurrentAxes',handles.b);
        image(imread ('Bluetemp.bmp'));
        axis off;
        
        handles.filename = 'RGBtemp';
        guidata(hObject,handles);
 

end

if handles.redcheckbox == 1 & handles.greencheckbox == 1 & handles.bluecheckbox == 0
 
    
    
    
    Ntotalred = handles.rednumber;
    Ntotalgreen = handles.greennumber;
    Nrg = handles.Xi1 + handles.Nrg;
    
    
    %non-colocolized red and green:
    
    Nrednc = Ntotalred - Nrg;
    Ngreennc = Ntotalgreen - Nrg;
    
    
    
    
    
    RGB1 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB2 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB3 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB = zeros(handles.xdimension, handles.ydimension, 3);
    
    X = ceil((handles.xdimension).*rand(Nrg, 1));
    Y = ceil((handles.ydimension).*rand(Nrg, 1));
    
    XX = ceil((handles.xdimension).*rand(Nrednc, 1));
    YY = ceil((handles.xdimension).*rand(Nrednc, 1));
    
    XXX = ceil((handles.xdimension).*rand(Ngreennc, 1));
    YYY = ceil((handles.xdimension).*rand(Ngreennc, 1));

    
    pixintred = zeros(Nrg, 1);
    pixintgreen = zeros(Nrg, 1);
    
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:Nrg
            
                x = i - X(l);
                y = j - Y(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixintred(l) = G(l)*handles.brightnessred;
                pixintgreen(l) = G(l)*handles.brightnessgreen;
                
            end     
            
            
        RGB1(i, j, 1) = sum(pixintred);
        RGB1(i, j, 2) = sum(pixintgreen);
       
        end
    end
    
    pixint = zeros(Nrednc, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:Nrednc
            
                x = i - XX(l);
                y = j - YY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessred;
                
            end     
            
        RGB2(i, j, 1) = sum(pixint);
               
        end
    end
    
    pixint = zeros(Ngreennc, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:Ngreennc
            
                x = i - XXX(l);
                y = j - YYY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessgreen;
                
            end     
            
        RGB3(i, j, 2) = sum(pixint);
               
        end
    end
    
    RGB = RGB1 + RGB2 + RGB3;
    
    
    emptymatrix = zeros(handles.xdimension, handles.ydimension);
    
        set(gcf,'CurrentAxes',handles.rgb);
        RedGreen = cat(3, RGB(:, :, 1), RGB(:, :, 2), emptymatrix);
        imwrite(RedGreen, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.r)
        Red = cat(3, RGB(:, :, 1), emptymatrix, emptymatrix);
        imwrite(Red, 'Redtemp.bmp');
        image(imread ('Redtemp.bmp'));
        axis off


        set(gcf,'CurrentAxes',handles.g)
        Green = cat(3, emptymatrix, RGB(:, :, 2), emptymatrix);
        imwrite(Green, 'Greentemp.bmp');
        image(imread ('Greentemp.bmp'));
        axis off
        
        
           
        set(gcf,'CurrentAxes',handles.b);
        image(imread ('logoMaxB.jpg'));
        axis off;
        
        handles.filename = 'RGBtemp';
        guidata(hObject,handles);
 
      
    
    
end


if handles.redcheckbox == 1 & handles.greencheckbox == 0 & handles.bluecheckbox == 1
    
    
    Ntotalred = handles.rednumber;
    Ntotalblue = handles.bluenumber;
    Nrb = handles.Xi2 + handles.Nrb;
    
    
    %non-colocolized red and blue:
    
    Nrednc = Ntotalred - Nrb;
    Nbluenc = Ntotalblue - Nrb;
    
    
    
    
    
    RGB1 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB2 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB3 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB = zeros(handles.xdimension, handles.ydimension, 3);
    
    X = ceil((handles.xdimension).*rand(Nrb, 1));
    Y = ceil((handles.ydimension).*rand(Nrb, 1));
    
    XX = ceil((handles.xdimension).*rand(Nrednc, 1));
    YY = ceil((handles.xdimension).*rand(Nrednc, 1));
    
    XXX = ceil((handles.xdimension).*rand(Nbluenc, 1));
    YYY = ceil((handles.xdimension).*rand(Nbluenc, 1));

    
    pixintred = zeros(Nrb, 1);
    pixintblue = zeros(Nrb, 1);
    
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:Nrb
            
                x = i - X(l);
                y = j - Y(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixintred(l) = G(l)*handles.brightnessred;
                pixintblue(l) = G(l)*handles.brightnessblue;
                
            end     
            
            
        RGB1(i, j, 1) = sum(pixintred);
        RGB1(i, j, 3) = sum(pixintblue);
       
        end
    end
    
    pixint = zeros(Nrednc, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:Nrednc
            
                x = i - XX(l);
                y = j - YY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessred;
                
            end     
            
        RGB2(i, j, 1) = sum(pixint);
               
        end
    end
    
    pixint = zeros(Nbluenc, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:Nbluenc
            
                x = i - XXX(l);
                y = j - YYY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessblue;
                
            end     
            
        RGB3(i, j, 3) = sum(pixint);
               
        end
    end
    
    RGB = RGB1 + RGB2 + RGB3;
    
    
    emptymatrix = zeros(handles.xdimension, handles.ydimension);
    
        set(gcf,'CurrentAxes',handles.rgb);
        RedBlue = cat(3, RGB(:, :, 1), emptymatrix, RGB(:, :, 3));
        imwrite(RedBlue, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.r)
        Red = cat(3, RGB(:, :, 1), emptymatrix, emptymatrix);
        imwrite(Red, 'Redtemp.bmp');
        image(imread ('Redtemp.bmp'));
        axis off


        set(gcf,'CurrentAxes',handles.b)
        Blue = cat(3, emptymatrix, emptymatrix, RGB(:, :, 3));
        imwrite(Blue, 'Bluetemp.bmp');
        image(imread ('Bluetemp.bmp'));
        axis off
        
        
           
        set(gcf,'CurrentAxes',handles.g);
        image(imread ('logoMaxG.jpg'));
        axis off;
        
        handles.filename = 'RGBtemp';
        guidata(hObject,handles);
 
      
    
    
end

if handles.redcheckbox == 0 & handles.greencheckbox == 1 & handles.bluecheckbox == 1
    
    
    Ntotalgreen = handles.greennumber;
    Ntotalblue = handles.bluenumber;
    Ngb = handles.Xi3 + handles.Ngb;
    
    
    %non-colocolized green and blue:
    
    Ngreennc = Ntotalgreen - Ngb;
    Nbluenc = Ntotalblue - Ngb;
    
    
    
    RGB1 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB2 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB3 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB = zeros(handles.xdimension, handles.ydimension, 3);
    
    X = ceil((handles.xdimension).*rand(Ngb, 1));
    Y = ceil((handles.ydimension).*rand(Ngb, 1));
    
    XX = ceil((handles.xdimension).*rand(Ngreennc, 1));
    YY = ceil((handles.xdimension).*rand(Ngreennc, 1));
    
    XXX = ceil((handles.xdimension).*rand(Nbluenc, 1));
    YYY = ceil((handles.xdimension).*rand(Nbluenc, 1));

    
    pixintgreen = zeros(Ngb, 1);
    pixintblue = zeros(Ngb, 1);
    
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:Ngb
            
                x = i - X(l);
                y = j - Y(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixintgreen(l) = G(l)*handles.brightnessgreen;
                pixintblue(l) = G(l)*handles.brightnessblue;
                
            end     
            
            
        RGB1(i, j, 2) = sum(pixintgreen);
        RGB1(i, j, 3) = sum(pixintblue);
       
        end
    end
    
    pixint = zeros(Ngreennc, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:Ngreennc
            
                x = i - XX(l);
                y = j - YY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessgreen;
                
            end     
            
        RGB2(i, j, 2) = sum(pixint);
               
        end
    end
    
    pixint = zeros(Nbluenc, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:Nbluenc
            
                x = i - XXX(l);
                y = j - YYY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessblue;
                
            end     
            
        RGB3(i, j, 3) = sum(pixint);
               
        end
    end
    
    RGB = RGB1 + RGB2 + RGB3;
    
    
    emptymatrix = zeros(handles.xdimension, handles.ydimension);
    
        set(gcf,'CurrentAxes',handles.rgb);
        GreenBlue = cat(3, emptymatrix, RGB(:, :, 2), RGB(:, :, 3));
        imwrite(GreenBlue, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.g)
        Green = cat(3, emptymatrix, RGB(:, :, 2), emptymatrix);
        imwrite(Green, 'Greentemp.bmp');
        image(imread ('Greentemp.bmp'));
        axis off


        set(gcf,'CurrentAxes',handles.b)
        Blue = cat(3, emptymatrix, emptymatrix, RGB(:, :, 3));
        imwrite(Blue, 'Bluetemp.bmp');
        image(imread ('Bluetemp.bmp'));
        axis off
        
        
           
        set(gcf,'CurrentAxes',handles.r);
        image(imread ('logoMaxR.jpg'));
        axis off;
        
        handles.filename = 'RGBtemp';
        guidata(hObject,handles);
 
      
    
    
end

if handles.redcheckbox == 1 & handles.greencheckbox == 1 & handles.bluecheckbox == 1
    
    
    
    
                curRed = poissrnd(handles.rednumber - handles.Xi1 - handles.Xi2 - handles.Xi6 - handles.Nrb - handles.Nrgb - handles.Nrg);
                curGreen = poissrnd(handles.greennumber - handles.Xi1 - handles.Xi3 - handles.Xi5 - handles.Nrg - handles.Nrgb - handles.Ngb);
                curBlue = poissrnd(handles.bluenumber - handles.Xi2 - handles.Xi3 - handles.Xi4 - handles.Nrb - handles.Ngb - handles.Nrgb);
                curRG = poissrnd(handles.Nrg + handles.Xi1 - handles.Xi4);
                curRB = poissrnd(handles.Nrb + handles.Xi2 - handles.Xi5);
                curGB = poissrnd(handles.Ngb + handles.Xi3 - handles.Xi6);
                curRGB = poissrnd(handles.Nrgb + handles.Xi4 + handles.Xi5 + handles.Xi6);
    
    
                set(handles.NgP, 'String', curGreen);
                set(handles.NrP, 'String', curRed);
                set(handles.NbP, 'String', curBlue);
                set(handles.NrbP, 'String', curRB);
                set(handles.NrgP, 'String', curRG);
                set(handles.NgbP, 'String', curGB);
                set(handles.NrgbP, 'String', curRGB);
    
     
    
  
        
    RGB1 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB2 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB3 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB4 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB5 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB6 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB7 = zeros(handles.xdimension, handles.ydimension, 3);
    RGB = zeros(handles.xdimension, handles.ydimension, 3);
    
    X = ceil((handles.xdimension).*rand(curRGB, 1));
    Y = ceil((handles.ydimension).*rand(curRGB, 1));
    
    XX = ceil((handles.xdimension).*rand(curRG, 1));
    YY = ceil((handles.xdimension).*rand(curRG, 1));
    
    XXX = ceil((handles.xdimension).*rand(curRB, 1));
    YYY = ceil((handles.xdimension).*rand(curRB, 1));
    
    XXXX = ceil((handles.xdimension).*rand(curGB, 1));
    YYYY = ceil((handles.xdimension).*rand(curGB, 1));
    
    XR = ceil((handles.xdimension).*rand(curRed, 1));
    YR = ceil((handles.ydimension).*rand(curRed, 1));

    XG = ceil((handles.ydimension).*rand(curGreen, 1));
    YG = ceil((handles.ydimension).*rand(curGreen, 1));
    
    XB = ceil((handles.ydimension).*rand(curBlue, 1));
    YB = ceil((handles.ydimension).*rand(curBlue, 1));
    
  
    pixintred = zeros(curRGB, 1);
    pixintgreen = zeros(curRGB, 1);
    pixintblue = zeros(curRGB, 1);
    
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:curRGB
            
                x = i - X(l);
                y = j - Y(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixintred(l) = G(l)*handles.brightnessred;
                pixintgreen(l) = G(l)*handles.brightnessgreen;
                pixintblue(l) = G(l)*handles.brightnessblue;
                
            end     
            
        RGB1(i, j, 1) = sum(pixintred);    
        RGB1(i, j, 2) = sum(pixintgreen);
        RGB1(i, j, 3) = sum(pixintblue);
       
        end
    end
    
    
    pixintred = zeros(curRG, 1);
    pixintgreen = zeros(curRG, 1);
    
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:curRG
            
                x = i - XX(l);
                y = j - YY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixintred(l) = G(l)*handles.brightnessred;
                pixintgreen(l) = G(l)*handles.brightnessgreen;
                
            end     
            
            
        RGB2(i, j, 1) = sum(pixintred);
        RGB2(i, j, 2) = sum(pixintgreen);
       
        end
    end
    
    
    pixintred = zeros(curRB, 1);
    pixintblue = zeros(curRB, 1);
    
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:curRB
            
                x = i - XXX(l);
                y = j - YYY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixintred(l) = G(l)*handles.brightnessred;
                pixintblue(l) = G(l)*handles.brightnessblue;
                
            end     
            
            
        RGB3(i, j, 1) = sum(pixintred);
        RGB3(i, j, 3) = sum(pixintblue);
       
        end
    end
    
    
    pixintgreen = zeros(curGB, 1);
    pixintblue = zeros(curGB, 1);
    
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
       
            for l = 1:curGB
            
                x = i - XXXX(l);
                y = j - YYYY(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixintgreen(l) = G(l)*handles.brightnessgreen;
                pixintblue(l) = G(l)*handles.brightnessblue;
                
            end     
            
            
        RGB4(i, j, 2) = sum(pixintgreen);
        RGB4(i, j, 3) = sum(pixintblue);
       
        end
    end
    
    
    pixint = zeros(curRed, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:curRed
            
                x = i - XR(l);
                y = j - YR(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessred;
                
            end     
            
        RGB5(i, j, 1) = sum(pixint);
               
        end
    end
    
    
    pixint = zeros(curGreen, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:curGreen
            
                x = i - XG(l);
                y = j - YG(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessgreen;
                
            end     
            
        RGB6(i, j, 2) = sum(pixint);
               
        end
    end
    
    
    pixint = zeros(curBlue, 1);
    for i = 1:handles.xdimension
        for j = 1:handles.ydimension
       
            for l = 1:curBlue
            
                x = i - XB(l);
                y = j - YB(l);

                G(l)= exp(-2*(x^2+y^2)/(handles.beamradius*handles.beamradius));
                
                pixint(l) = G(l)*handles.brightnessblue;
                
            end     
            
        RGB7(i, j, 3) = sum(pixint);
               
        end
    end
    
    
    
    RGB = RGB1 + RGB2 + RGB3 + RGB4 + RGB5 + RGB6+ RGB7;
    
    
   emptymatrix = zeros(handles.xdimension, handles.ydimension);
    
        set(gcf,'CurrentAxes',handles.rgb);
        RedGreenBlue = cat(3, RGB(:, :, 1), RGB(:, :, 2), RGB(:, :, 3));
        imwrite(RedGreenBlue, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.g)
        Green = cat(3, emptymatrix, RGB(:, :, 2), emptymatrix);
        imwrite(Green, 'Greentemp.bmp');
        image(imread ('Greentemp.bmp'));
        axis off


        set(gcf,'CurrentAxes',handles.b)
        Blue = cat(3, emptymatrix, emptymatrix, RGB(:, :, 3));
        imwrite(Blue, 'Bluetemp.bmp');
        image(imread ('Bluetemp.bmp'));
        axis off
        
        
        set(gcf,'CurrentAxes',handles.r)
        Red = cat(3, RGB(:, :, 1), emptymatrix, emptymatrix);
        imwrite(Red, 'Redtemp.bmp');
        image(imread ('Redtemp.bmp'));
        axis off
        
        handles.filename = 'RGBtemp';
        guidata(hObject,handles);
   
    
    
end


guidata(hObject,handles);





% --- Executes on button press in reactionscheme.
function reactionscheme_Callback(hObject, eventdata, handles)
% hObject    handle to reactionscheme (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

figure (1)
image(imread('reactions.jpg'));
axis off




% --- Executes on selection change in choosemodel.
function choosemodel_Callback(hObject, eventdata, handles)
% hObject    handle to choosemodel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = get(hObject,'String') returns choosemodel contents as cell array
%        contents{get(hObject,'Value')} returns selected item from choosemodel

handles.str = get(hObject, 'String');
handles.val = get(hObject,'Value');

guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function choosemodel_CreateFcn(hObject, eventdata, handles)
% hObject    handle to choosemodel (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


handles.str = get(hObject, 'String');
handles.val = get(hObject,'Value');

guidata(hObject,handles);



function g0_Callback(hObject, eventdata, handles)
% hObject    handle to g0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of g0 as text
%        str2double(get(hObject,'String')) returns contents of g0 as a double

g0 = str2double(get(hObject,'string'));

            if isnan(g0)
                errordlg('You must enter a numeric value','Bad Input','modal')
            end

    handles.g0 = g0;
    set(handles.g0fit, 'String', g0);
     
    
    guidata(hObject,handles);





% --- Executes during object creation, after setting all properties.
function g0_CreateFcn(hObject, eventdata, handles)
% hObject    handle to g0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function w_Callback(hObject, eventdata, handles)
% hObject    handle to w (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of w as text
%        str2double(get(hObject,'String')) returns contents of w as a double

w = str2double(get(hObject,'string'));

            if isnan(w)
                errordlg('You must enter a numeric value','Bad Input','modal')
            end

    handles.w = w;
    set(handles.wfit, 'String', w);
     
    
    guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function w_CreateFcn(hObject, eventdata, handles)
% hObject    handle to w (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function ginf_Callback(hObject, eventdata, handles)
% hObject    handle to ginf (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ginf as text
%        str2double(get(hObject,'String')) returns contents of ginf as a double

ginf = str2double(get(hObject,'string'));

            if isnan(ginf)
                errordlg('You must enter a numeric value','Bad Input','modal')
            end

    handles.ginf = ginf;
    set(handles.ginffit, 'String', ginf);
     
    
    guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function ginf_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ginf (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes on button press in pushtofit.
function pushtofit_Callback(hObject, eventdata, handles)
% hObject    handle to pushtofit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



switch handles.str{handles.val};
    
    case 'Choose...' % User selection
        
        errordlg('You need to choose a fitting model','Bad Input','modal')
        
    case 'ICS red' % User selection
        
        
        if isempty(handles.filename) ~= 1
            if isdir(handles.filename) ~= 1
                mkdir(handles.filename);
            end
        end
            
        
        
           
           imag = imread('Redtemp.bmp');
           
           R = double(imag(:, :, 1));
           
           %gets dimensions of orig matrix
           SR = size(R);
        
           %calculates average of all matrix entries
           avgR = sum(sum(R))/(SR(1)*SR(2));
       
           
           gR = (ifft2((fft2(R).*conj(fft2(R))))/(avgR^2*SR(1)*SR(2)))-1;
           
           range = handles.range;
           
           for i = 1:range
               for j = 1:range
                   gRnew(i, j) = gR(i, j);
               end
           end
           
           %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
           tempvalueR = gRnew(1, 1);
            gRnew(1, 1) = gRnew(1, 2);
          
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
            AutoGinitialR = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            AutoGfitR = lsqcurvefit(@Autocorrelation, AutoGinitialR, delta, gRnew, lb, ub, options);

            gRfit = Autocorrelation(AutoGfitR, delta);
            
            pathname = handles.filename;
            filename1 = 'ACr.txt';
            filename2 = 'ACrFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
            gRnew(1, 1) = tempvalueR;
                     
            dlmwrite(File1, gRnew, 'delimiter', '\t');
            dlmwrite(File2, gRfit, 'delimiter', '\t');
            
            for mm = 1:handles.range
                newcorredfit1(mm) = gRfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorred1(mm) = gRnew(mm+1, 1);
            end
            
            
            
            figure('Name','Autocorrelation Red Y','NumberTitle','off')
            plot(delta1,newcorred1,'or',...
                delta,newcorredfit1,'--r',...
                'LineWidth',2)
            if newcorred1(1) >= newcorredfit1(1)
                axis([0 range 0 newcorred1(1)])
            else
                axis([0 range 0 newcorredfit1(1)])
            end
                    
               
            
            
           
            guidata(hObject,handles);
            
           
            
       %     set(handles.timer, 'String', ceil(toc));
      
    case 'ICS green' % User selection
   
        
        if isempty(handles.filename) ~= 1
            if isdir(handles.filename) ~= 1
                mkdir(handles.filename);
            end
        end
        
        imag = imread('Greentemp.bmp');
           
           G = double(imag(:, :, 2));
           
           %gets dimensions of orig matrix
           SG = size(G);
        
           %calculates average of all matrix entries
           avgG = sum(sum(G))/(SG(1)*SG(2));
       
           
           gG = (ifft2((fft2(G).*conj(fft2(G))))/(avgG^2*SG(1)*SG(2)))-1;
           
           range = handles.range;
           
           for i = 1:range
               for j = 1:range
                   gGnew(i, j) = gG(i, j);
               end
           end
           
           %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
           tempvalueG = gGnew(1, 1);
            gGnew(1, 1) = gGnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
            AutoGinitialG = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            AutoGfitG = lsqcurvefit(@Autocorrelation, AutoGinitialG, delta, gGnew, lb, ub, options);

            gGfit = Autocorrelation(AutoGfitG, delta);
            
            pathname = handles.filename;
            filename1 = 'ACg.txt';
            filename2 = 'ACgFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
            gGnew(1, 1) = tempvalueG;
                     
            dlmwrite(File1, gGnew, 'delimiter', '\t');
            dlmwrite(File2, gGfit, 'delimiter', '\t');
            
            
            for mm = 1:handles.range
                newcorgreenfit1(mm) = gGfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorgreen1(mm) = gGnew(mm+1, 1);
            end
            
            
            
            figure('Name','Autocorrelation Green Y','NumberTitle','off')
            plot(delta1,newcorgreen1,'og',...
                delta,newcorgreenfit1,'--g',...
                'LineWidth',2)
            if newcorgreen1(1) >= newcorgreenfit1(1)
                axis([0 range 0 newcorgreen1(1)])
            else
                axis([0 range 0 newcorgreenfit1(1)])
            end
                    
            
                       
            guidata(hObject,handles);
           
        case 'ICS blue' % User selection
            
            if isempty(handles.filename) ~= 1
                if isdir(handles.filename) ~= 1
                    mkdir(handles.filename);
                end
            end
            
            
            
        imag = imread('Bluetemp.bmp');
           
           B = double(imag(:, :, 3));
           
           %gets dimensions of orig matrix
           SB = size(B);
        
           %calculates average of all matrix entries
           avgB = sum(sum(B))/(SB(1)*SB(2));
       
           
           gB = (ifft2((fft2(B).*conj(fft2(B))))/(avgB^2*SB(1)*SB(2)))-1;
           
           range = handles.range;
           
           for i = 1:range
               for j = 1:range
                   gBnew(i, j) = gB(i, j);
               end
           end
           
           %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
           tempvalueB = gBnew(1, 1);
            gBnew(1, 1) = gBnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
            AutoGinitialB = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            AutoGfitB = lsqcurvefit(@Autocorrelation, AutoGinitialB, delta, gBnew, lb, ub, options);

            gBfit = Autocorrelation(AutoGfitB, delta);
            
            pathname = handles.filename;
            filename1 = 'ACb.txt';
            filename2 = 'ACbFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
            gBnew(1, 1) = tempvalueB;
                     
            dlmwrite(File1, gBnew, 'delimiter', '\t');
            dlmwrite(File2, gBfit, 'delimiter', '\t');
            
            
            for mm = 1:handles.range
                newcorbluefit1(mm) = gBfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorblue1(mm) = gBnew(mm+1, 1);
            end
            
            
            
            figure('Name','Autocorrelation Blue Y','NumberTitle','off')
            plot(delta1,newcorblue1,'ob',...
                delta,newcorbluefit1,'--b',...
                'LineWidth',2)
            if newcorblue1(1) >= newcorbluefit1(1)
                axis([0 range 0 newcorblue1(1)])
            else
                axis([0 range 0 newcorbluefit1(1)])
            end
           
            guidata(hObject,handles);
        
                
        case 'XCS red/green' % User selection
            
            if isempty(handles.filename) ~= 1
                if isdir(handles.filename) ~= 1
                    mkdir(handles.filename);
                end
            end
            
            
            
            
            imag1 = imread('Redtemp.bmp');
            imag2 = imread('Greentemp.bmp');
           
           R = double(imag1(:, :, 1));
           G = double(imag2(:, :, 2));
           
           %gets dimensions of orig matrix
           SR = size(R);
        
           %calculates average of all matrix entries
           avgR = sum(sum(R))/(SR(1)*SR(2));
           avgG = sum(sum(G))/(SR(1)*SR(2));
       
           
           gRG = (ifft2((fft2(R).*conj(fft2(G))))/(avgR*avgG*SR(1)*SR(2)))-1;
           
           range = handles.range;
           
           for i = 1:range
               for j = 1:range
                   gRGnew(i, j) = gRG(i, j);
               end
           end
           
           %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
            tempvalueRG = gRGnew(1, 1);
            gRGnew(1, 1) = gRGnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
            CrossGinitialRG = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            CrossGfitRG = lsqcurvefit(@Crosscorrelation, CrossGinitialRG, delta, gRGnew, lb, ub, options);

            gRGfit = Crosscorrelation(CrossGfitRG, delta);
            
            pathname = handles.filename;
            filename1 = 'XCrg.txt';
            filename2 = 'XCrgFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
            gRGnew(1, 1) = tempvalueRG;
                     
            dlmwrite(File1, gRGnew, 'delimiter', '\t');
            dlmwrite(File2, gRGfit, 'delimiter', '\t');
            
            
            for mm = 1:handles.range
                newcorrgfit1(mm) = gRGfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorrg1(mm) = gRGnew(mm+1, 1);
            end
            
            
            
            figure('Name','Crosscorrelation Red Green Y','NumberTitle','off')
            plot(delta1,newcorrg1,'oy',...
                delta,newcorrgfit1,'--y',...
                'LineWidth',2)
            if newcorrg1(1) >= newcorrgfit1(1)
                axis([0 range 0 newcorrg1(1)])
            else
                axis([0 range 0 newcorrgfit1(1)])
            end
            
                       
            guidata(hObject,handles);
        
            
        case 'XCS red/blue' % User selection
            
            if isempty(handles.filename) ~= 1
                if isdir(handles.filename) ~= 1
                    mkdir(handles.filename);
                end
            end
            
            
            imag1 = imread('Redtemp.bmp');
            imag2 = imread('Bluetemp.bmp');
           
           R = double(imag1(:, :, 1));
           B = double(imag2(:, :, 3));
           
           %gets dimensions of orig matrix
           SR = size(R);
        
           %calculates average of all matrix entries
           avgR = sum(sum(R))/(SR(1)*SR(2));
           avgB = sum(sum(B))/(SR(1)*SR(2));
       
           
           gRB = (ifft2((fft2(R).*conj(fft2(B))))/(avgR*avgB*SR(1)*SR(2)))-1;
           
           range = handles.range;
           
           for i = 1:range
               for j = 1:range
                   gRBnew(i, j) = gRB(i, j);
               end
           end
           
           
           
           %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
            tempvalueRB = gRBnew(1, 1);
            gRBnew(1, 1) = gRBnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
            CrossGinitialRB = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            CrossGfitRB = lsqcurvefit(@Crosscorrelation, CrossGinitialRB, delta, gRBnew, lb, ub, options);

            gRBfit = Crosscorrelation(CrossGfitRB, delta);
            
            pathname = handles.filename;
            filename1 = 'XCrb.txt';
            filename2 = 'XCrbFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
            gRBnew(1, 1) = tempvalueRB;
                     
            dlmwrite(File1, gRBnew, 'delimiter', '\t');
            dlmwrite(File2, gRBfit, 'delimiter', '\t');
            
            for mm = 1:handles.range
                newcorrbfit1(mm) = gRBfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorrb1(mm) = gRBnew(mm+1, 1);
            end
            
            
            
            figure('Name','Crosscorrelation Red Blue Y','NumberTitle','off')
            plot(delta1,newcorrb1,'om',...
                delta,newcorrbfit1,'--m',...
                'LineWidth',2)
            if newcorrb1(1) >= newcorrbfit1(1)
                axis([0 range 0 newcorrb1(1)])
            else
                axis([0 range 0 newcorrbfit1(1)])
            end
            
                       
            guidata(hObject,handles);
            
            
        case 'XCS green/blue' % User selection
            
            if isempty(handles.filename) ~= 1
                if isdir(handles.filename) ~= 1
                    mkdir(handles.filename);
                end
            end
            
            
            imag1 = imread('Greentemp.bmp');
            imag2 = imread('Bluetemp.bmp');
           
           G = double(imag1(:, :, 2));
           B = double(imag2(:, :, 3));
           
           %gets dimensions of orig matrix
           SG = size(G);
        
           %calculates average of all matrix entries
           avgG = sum(sum(G))/(SG(1)*SG(2));
           avgB = sum(sum(B))/(SG(1)*SG(2));
       
           
           gGB = (ifft2((fft2(G).*conj(fft2(B))))/(avgG*avgB*SG(1)*SG(2)))-1;
           
           range = handles.range;
           
           for i = 1:range
               for j = 1:range
                   gGBnew(i, j) = gGB(i, j);
               end
           end
           
           %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
            tempvalueGB = gGBnew(1, 1);
            gGBnew(1, 1) = gGBnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
            CrossGinitialGB = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            CrossGfitGB = lsqcurvefit(@Crosscorrelation, CrossGinitialGB, delta, gGBnew, lb, ub, options);

            gGBfit = Crosscorrelation(CrossGfitGB, delta);
            
            
            pathname = handles.filename;
            filename1 = 'XCgb.txt';
            filename2 = 'XCgbFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
            gGBnew(1, 1) = tempvalueGB;
                     
            dlmwrite(File1, gGBnew, 'delimiter', '\t');
            dlmwrite(File2, gGBfit, 'delimiter', '\t');
            
            for mm = 1:handles.range
                newcorgbfit1(mm) = gGBfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorgb1(mm) = gGBnew(mm+1, 1);
            end
            
            
            
            figure('Name','Crosscorrelation Green Blue Y','NumberTitle','off')
            plot(delta1,newcorgb1,'oc',...
                delta,newcorgbfit1,'--c',...
                'LineWidth',2)
            if newcorgb1(1) >= newcorgbfit1(1)
                axis([0 range 0 newcorgb1(1)])
            else
                axis([0 range 0 newcorgbfit1(1)])
            end
                   
            guidata(hObject,handles);      
        
        case 'Triple ICS' % User selection        
        
            
            
           if isempty(handles.filename) ~= 1
                if isdir(handles.filename) ~= 1
                    mkdir(handles.filename);
                end
           end         
            
           
           imag = imread('RGBtemp.bmp');
           
           
           R = double(imag(:, :, 1));
           G = double(imag(:, :, 2));
           B = double(imag(:, :, 3));
           
           %gets dimensions of orig matrix
           SG = size(R);
        
           %calculates average of all matrix entries
           avgR = sum(sum(R))/(SG(1)*SG(2));
           avgG = sum(sum(G))/(SG(1)*SG(2));
           avgB = sum(sum(B))/(SG(1)*SG(2));
           
           
            deltaimagred = R - avgR;
            deltaimaggreen = G - avgG;
            deltaimagblue = B - avgB;
           
            %--------------------------------------------------------------
            % Calculating triple correlation function through bispectrum


            %--------------------------------------------------------------
            % Calculating Fast Fourier Transform of deltasignal
    
            fftdeltaimagred = fftn(deltaimagred);
            fftdeltaimaggreen = fftn(deltaimaggreen);
            fftdeltaimagblue = fftn(deltaimagblue);
    
            sfftdeltaimagred = fftshift(fftdeltaimagred);
            sfftdeltaimaggreen = fftshift(fftdeltaimaggreen);
            sfftdeltaimagblue = fftshift(fftdeltaimagblue);
    
            figure('Name','Fourier Transform of RED','NumberTitle','off')
            surfc(abs(sfftdeltaimagred))
            
            
            prompt = {'Enter starting point:'};
            dlg_title = 'Input for calculating bispectrum';
            num_lines = 1;
            def = {'64'};
            lowlim = inputdlg(prompt,dlg_title,num_lines,def);
            lowlim = str2double(lowlim);
            
            highlim = SG(1) - lowlim;

            lim = highlim - lowlim;

            nhlf = SG(1)/2;
            nhlfp = nhlf+1;
            nhlfm = nhlf-1;

            nbi = lim;
            nbihlfp = nbi/2+1;
            
            r1 = zeros(lim, lim, lim, lim);
            
            tic
                
                for v1 = (-nhlf+lowlim):0
                    for u1 = (-nhlf+lowlim)-(v1-1):(nhlfm-lowlim)
                        for v2 = (-nhlf+lowlim):(nhlfm-lowlim)
                            for u2 = (-nhlf+lowlim):(nhlfm-lowlim)
                                if abs(u2+v2) <= nhlfm
                                    
                                    r1(nbihlfp + v1, nbihlfp + u1, nbihlfp + v2, nbihlfp + u2) = sfftdeltaimagred(nhlfp + u1, nhlfp + u2).*sfftdeltaimaggreen(nhlfp + v1, nhlfp + v2).*conj(sfftdeltaimagblue(nhlfp + u1 + v1, nhlfp + u2 + v2))./(SG(1)*SG(2));
                                    
                                end
                            end
                        end
                    end
                end

                


                
                for v1 = 1:(nhlfm-lowlim)
                    for u1 = (-nhlf+lowlim):(nhlfm-lowlim)-v1
                        for v2 = (-nhlf+lowlim):(nhlfm-lowlim)
                            for u2 = (-nhlf+lowlim):(nhlfm-lowlim)
                                if abs(u2+v2) <= nhlfm
                                    
                                    r1(nbihlfp + v1, nbihlfp + u1, nbihlfp + v2, nbihlfp + u2) = sfftdeltaimagred(nhlfp + u1, nhlfp + u2).*sfftdeltaimaggreen(nhlfp + v1, nhlfp + v2).*conj(sfftdeltaimagblue(nhlfp + u1 + v1, nhlfp + u2 + v2))./(SG(1)*SG(2));
                                    
                                end
                            end
                        end
                    end
                end
                toc
                
                
                figure('Name','Bispectrum','NumberTitle','off')
                
                colormap hsv
    
                
                bispectdisp = abs(r1(:, :, nbihlfp, nbihlfp));
                surfc(bispectdisp)
                
    
    % End of calculating bispectrum
    %----------------------------------------------------------------------
    
    
    
    %----------------------------------------------------------------------
    % Calculating triple correlation function
    
    
    bispectorig = fftshift(r1);   
    
    tricorr = ifftn(bispectorig).*((lim^4)/(SG(1)^2*SG(2)^2));   %compute the triple correlation (inverse FFT of bispectrum)
    
    tricorrnorm = tricorr/(avgR*avgG*avgB);
    
    figure('Name','Triple Correlation Function 3D','NumberTitle','off')
    tricorrdisp = fftshift(abs(tricorrnorm(:,:,1, 1)));
    surfc(tricorrdisp)
    colormap hsv
    
    
    
    
            prompt = {'Enter number of pixels:'};
            dlg_title = 'Fitting range';
            num_lines = 1;
            def = {'20'};
            range = inputdlg(prompt,dlg_title,num_lines,def);
            range = str2double(range);
            
            
            for ii = 1:range
        for jj = 1:range
            
            testmatrix1(ii, jj) = real(tricorrnorm(ii, jj, 1, 1));
            testmatrix2(ii, jj) = real(tricorrnorm(1, ii, jj, 1));
            testmatrix3(ii, jj) = real(tricorrnorm(1, 1, ii, jj));
            testmatrix4(ii, jj) = real(tricorrnorm(1, ii, 1, jj));
            testmatrix5(ii, jj) = real(tricorrnorm(ii, 1, jj, 1));
            testmatrix6(ii, jj) = real(tricorrnorm(ii, 1, 1, jj));
            
        end
    end
    
       
    
    for mm = 1:range
        
         newtricorre1(mm) = testmatrix1(1, mm);
         newtricorre2(mm) = testmatrix1(mm, 1);
         newtricorre3(mm) = testmatrix1(mm, mm);
         
         newtricorre4(mm) = testmatrix2(1, mm);
         newtricorre5(mm) = testmatrix2(mm, 1);
         
         newtricorre6(mm) = testmatrix3(1, mm);
         newtricorre7(mm) = testmatrix3(mm, 1);
         newtricorre8(mm) = testmatrix3(mm, mm);
         
         newtricorre9(mm) = testmatrix4(1, mm);
         newtricorre10(mm) = testmatrix4(mm, 1);
         
         newtricorre11(mm) = testmatrix5(1, mm);
         newtricorre12(mm) = testmatrix5(mm, 1);
         
         newtricorre13(mm) = testmatrix6(1, mm);
         newtricorre14(mm) = testmatrix6(mm, 1);
         
    end
    
 %   disp(newtricorre1)
 %   disp(newtricorre2)
 %   disp(newtricorre3)
 %   disp(newtricorre4)
 %   disp(newtricorre5)
 %   disp(newtricorre6)
 %   disp(newtricorre7)
 %   disp(newtricorre8)
 %   disp(newtricorre9)
 %   disp(newtricorre10)
 %   disp(newtricorre11)
 %   disp(newtricorre12)
 %   disp(newtricorre13)
 %   disp(newtricorre14)
    
    
    newt = ((newtricorre1+newtricorre2+newtricorre3+newtricorre4+newtricorre5+newtricorre6+newtricorre7+newtricorre8+newtricorre9+newtricorre10+newtricorre11+newtricorre12+newtricorre13+newtricorre14)/14)';
    
    
    
    % End of calculating triple correlation function
    %----------------------------------------------------------------------
    
    
% End of calculating triple correlation function through bispectrum
%--------------------------------------------------------------------------
            correctionw = SG(1)/lim;
            delta = [0:range-1]; 
            TripleGinitialRGB = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            TripleGfitRGB = lsqcurvefit(@Gausshalf, TripleGinitialRGB, delta, newt, lb, ub, options);

            TripleRGBfit = Gausshalf(TripleGfitRGB, delta);
            
            
            pathname = handles.filename;
            filename1 = 'TripleCrgb.txt';
            filename2 = 'TripleCrgbFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
        
                     
            dlmwrite(File1, newt, 'delimiter', '\t');
            dlmwrite(File2, TripleRGBfit, 'delimiter', '\t');
            
            
            figure('Name','Triple Correlation Function','NumberTitle','off')
            plot(delta,newt,'ok',...
                delta,TripleRGBfit,'--k',...
                'LineWidth',2)
            
                   
            guidata(hObject,handles);     
            
            
            
            case 'All' % User selection
                
                
                if isempty(handles.filename) ~= 1
                    if isdir(handles.filename) ~= 1
                        mkdir(handles.filename);
                    end
                end
            
            
            imag = imread('RGBtemp.bmp');
           
           
           R = double(imag(:, :, 1));
           G = double(imag(:, :, 2));
           B = double(imag(:, :, 3));
           
           
           if sum(sum(R)) ~= 0
               
                   %gets dimensions of orig matrix
               SR = size(R);

               %calculates average of all matrix entries
               avgR = sum(sum(R))/(SR(1)*SR(2));


               gR = (ifft2((fft2(R).*conj(fft2(R))))/(avgR^2*SR(1)*SR(2)))-1;

               range = handles.range;

               for i = 1:range
                   for j = 1:range
                       gRnew(i, j) = gR(i, j);
                   end
               end

            %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
           tempvalueR = gRnew(1, 1);
            gRnew(1, 1) = gRnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
                AutoGinitialR = [handles.g0, handles.w, handles.ginf];
                lb = [0, 0, -1000];
                ub = [10000000, 100000000, 1000];

                options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
                AutoGfitR = lsqcurvefit(@Autocorrelation, AutoGinitialR, delta, gRnew, lb, ub, options);

                gRfit = Autocorrelation(AutoGfitR, delta);

                pathname = handles.filename;
                filename1 = 'ACr.txt';
                filename2 = 'ACrFit.txt';
                File1 = fullfile(pathname,filename1);
                File2 = fullfile(pathname,filename2);

                gRnew(1, 1) = tempvalueR;
                     
            dlmwrite(File1, gRnew, 'delimiter', '\t');
            dlmwrite(File2, gRfit, 'delimiter', '\t');
            
            for mm = 1:handles.range
                newcorredfit1(mm) = gRfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorred1(mm) = gRnew(mm+1, 1);
            end
            
            
            
            figure('Name','Autocorrelation Red Y','NumberTitle','off')
            plot(delta1,newcorred1,'or',...
                delta,newcorredfit1,'--r',...
                'LineWidth',2)
            if newcorred1(1) >= newcorredfit1(1)
                axis([0 range 0 newcorred1(1)])
            else
                axis([0 range 0 newcorredfit1(1)])
            end
                    
               
            
            guidata(hObject,handles);
           end
           
           
           
           
           
           if sum(sum(G)) ~= 0
               
               %gets dimensions of orig matrix
           SG = size(G);
        
           %calculates average of all matrix entries
           avgG = sum(sum(G))/(SG(1)*SG(2));
       
           
           gG = (ifft2((fft2(G).*conj(fft2(G))))/(avgG^2*SG(1)*SG(2)))-1;
           
           range = handles.range;
           
           for i = 1:range
               for j = 1:range
                   gGnew(i, j) = gG(i, j);
               end
           end
           
           %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
           tempvalueG = gGnew(1, 1);
            gGnew(1, 1) = gGnew(1, 2);
            
            delta = [0:range-1; 0:range-1]; 
            delta1 = [1:range-1; 1:range-1];
            AutoGinitialG = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            AutoGfitG = lsqcurvefit(@Autocorrelation, AutoGinitialG, delta, gGnew, lb, ub, options);

            gGfit = Autocorrelation(AutoGfitG, delta);
            
            pathname = handles.filename;
            filename1 = 'ACg.txt';
            filename2 = 'ACgFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
            gGnew(1, 1) = tempvalueG;
                     
            dlmwrite(File1, gGnew, 'delimiter', '\t');
            dlmwrite(File2, gGfit, 'delimiter', '\t');
            
            
            for mm = 1:handles.range
                newcorgreenfit1(mm) = gGfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorgreen1(mm) = gGnew(mm+1, 1);
            end
            
            
            
            figure('Name','Autocorrelation Green Y','NumberTitle','off')
            plot(delta1,newcorgreen1,'og',...
                delta,newcorgreenfit1,'--g',...
                'LineWidth',2)
            if newcorgreen1(1) >= newcorgreenfit1(1)
                axis([0 range 0 newcorgreen1(1)])
            else
                axis([0 range 0 newcorgreenfit1(1)])
            end
                    
                      
            guidata(hObject,handles);
               
           end
           
           
           
           
           if sum(sum(B)) ~= 0
               
               %gets dimensions of orig matrix
           SB = size(B);
        
           %calculates average of all matrix entries
           avgB = sum(sum(B))/(SB(1)*SB(2));
       
           
           gB = (ifft2((fft2(B).*conj(fft2(B))))/(avgB^2*SB(1)*SB(2)))-1;
           
           range = handles.range;
           
           for i = 1:range
               for j = 1:range
                   gBnew(i, j) = gB(i, j);
               end
           end
           
           %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
           tempvalueB = gBnew(1, 1);
            gBnew(1, 1) = gBnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
            AutoGinitialB = [handles.g0, handles.w, handles.ginf];
            lb = [0, 0, -1000];
            ub = [10000000, 100000000, 1000];

            options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
            AutoGfitB = lsqcurvefit(@Autocorrelation, AutoGinitialB, delta, gBnew, lb, ub, options);

            gBfit = Autocorrelation(AutoGfitB, delta);
            
            pathname = handles.filename;
            filename1 = 'ACb.txt';
            filename2 = 'ACbFit.txt';
            File1 = fullfile(pathname,filename1);
            File2 = fullfile(pathname,filename2);
            
            gBnew(1, 1) = tempvalueB;
                     
            dlmwrite(File1, gBnew, 'delimiter', '\t');
            dlmwrite(File2, gBfit, 'delimiter', '\t');
            
            
            for mm = 1:handles.range
                newcorbluefit1(mm) = gBfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorblue1(mm) = gBnew(mm+1, 1);
            end
            
            
            
            figure('Name','Autocorrelation Blue Y','NumberTitle','off')
            plot(delta1,newcorblue1,'ob',...
                delta,newcorbluefit1,'--b',...
                'LineWidth',2)
            if newcorblue1(1) >= newcorbluefit1(1)
                axis([0 range 0 newcorblue1(1)])
            else
                axis([0 range 0 newcorbluefit1(1)])
            end
           
            guidata(hObject,handles);
        
              
           end
           
           
           
           if sum(sum(R)) ~= 0  && sum(sum(G)) ~= 0
               
                   %gets dimensions of orig matrix
               SR = size(R);

               %calculates average of all matrix entries
               avgR = sum(sum(R))/(SR(1)*SR(2));
               avgG = sum(sum(G))/(SR(1)*SR(2));


               gRG = (ifft2((fft2(R).*conj(fft2(G))))/(avgR*avgG*SR(1)*SR(2)))-1;

               range = handles.range;

               for i = 1:range
                   for j = 1:range
                       gRGnew(i, j) = gRG(i, j);
                   end
               end

            %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
            tempvalueRG = gRGnew(1, 1);
            gRGnew(1, 1) = gRGnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
                CrossGinitialRG = [handles.g0, handles.w, handles.ginf];
                lb = [0, 0, -1000];
                ub = [10000000, 100000000, 1000];

                options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
                CrossGfitRG = lsqcurvefit(@Crosscorrelation, CrossGinitialRG, delta, gRGnew, lb, ub, options);

                gRGfit = Crosscorrelation(CrossGfitRG, delta);

                pathname = handles.filename;
                filename1 = 'XCrg.txt';
                filename2 = 'XCrgFit.txt';
                File1 = fullfile(pathname,filename1);
                File2 = fullfile(pathname,filename2);

                gRGnew(1, 1) = tempvalueRG;
                     
            dlmwrite(File1, gRGnew, 'delimiter', '\t');
            dlmwrite(File2, gRGfit, 'delimiter', '\t');
            
            
            for mm = 1:handles.range
                newcorrgfit1(mm) = gRGfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorrg1(mm) = gRGnew(mm+1, 1);
            end
            
            
            
            figure('Name','Crosscorrelation Red Green Y','NumberTitle','off')
            plot(delta1,newcorrg1,'oy',...
                delta,newcorrgfit1,'--y',...
                'LineWidth',2)
            if newcorrg1(1) >= newcorrgfit1(1)
                axis([0 range 0 newcorrg1(1)])
            else
                axis([0 range 0 newcorrgfit1(1)])
            end
            


                guidata(hObject,handles);

             
           end
           
           
           
           if sum(sum(R)) ~= 0  && sum(sum(B)) ~= 0
               
               
               
               %gets dimensions of orig matrix
               SR = size(R);

               %calculates average of all matrix entries
               avgR = sum(sum(R))/(SR(1)*SR(2));
               avgB = sum(sum(B))/(SR(1)*SR(2));


               gRB = (ifft2((fft2(R).*conj(fft2(B))))/(avgR*avgB*SR(1)*SR(2)))-1;

               range = handles.range;

               for i = 1:range
                   for j = 1:range
                       gRBnew(i, j) = gRB(i, j);
                   end
               end

                %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
            tempvalueRB = gRBnew(1, 1);
            gRBnew(1, 1) = gRBnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
                CrossGinitialRB = [handles.g0, handles.w, handles.ginf];
                lb = [0, 0, -1000];
                ub = [10000000, 100000000, 1000];

                options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
                CrossGfitRB = lsqcurvefit(@Crosscorrelation, CrossGinitialRB, delta, gRBnew, lb, ub, options);

                gRBfit = Crosscorrelation(CrossGfitRB, delta);

                pathname = handles.filename;
                filename1 = 'XCrb.txt';
                filename2 = 'XCrbFit.txt';
                File1 = fullfile(pathname,filename1);
                File2 = fullfile(pathname,filename2);

                gRBnew(1, 1) = tempvalueRB;
                     
            dlmwrite(File1, gRBnew, 'delimiter', '\t');
            dlmwrite(File2, gRBfit, 'delimiter', '\t');
            
            for mm = 1:handles.range
                newcorrbfit1(mm) = gRBfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorrb1(mm) = gRBnew(mm+1, 1);
            end
            
            
            
            figure('Name','Crosscorrelation Red Blue Y','NumberTitle','off')
            plot(delta1,newcorrb1,'om',...
                delta,newcorrbfit1,'--m',...
                'LineWidth',2)
            if newcorrb1(1) >= newcorrbfit1(1)
                axis([0 range 0 newcorrb1(1)])
            else
                axis([0 range 0 newcorrbfit1(1)])
            end
            
                guidata(hObject,handles);
               
               
               
               
           end
               
                
           
           if sum(sum(G)) ~= 0  && sum(sum(B)) ~= 0



               %gets dimensions of orig matrix
               SG = size(G);

               %calculates average of all matrix entries
               avgG = sum(sum(G))/(SG(1)*SG(2));
               avgB = sum(sum(B))/(SG(1)*SG(2));


               gGB = (ifft2((fft2(G).*conj(fft2(B))))/(avgG*avgB*SG(1)*SG(2)))-1;

               range = handles.range;

               for i = 1:range
                   for j = 1:range
                       gGBnew(i, j) = gGB(i, j);
                   end
               end

            %Removing the value of g(0, 0) by assigning to it the adjacent
           %value g(1 ,1)
            tempvalueGB = gGBnew(1, 1);
            gGBnew(1, 1) = gGBnew(1, 2);
           
            delta = [0:range-1; 0:range-1];
            delta1 = [1:range-1; 1:range-1];
                CrossGinitialGB = [handles.g0, handles.w, handles.ginf];
                lb = [0, 0, -1000];
                ub = [10000000, 100000000, 1000];

                options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
                CrossGfitGB = lsqcurvefit(@Crosscorrelation, CrossGinitialGB, delta, gGBnew, lb, ub, options);

                gGBfit = Crosscorrelation(CrossGfitGB, delta);


                pathname = handles.filename;
                filename1 = 'XCgb.txt';
                filename2 = 'XCgbFit.txt';
                File1 = fullfile(pathname,filename1);
                File2 = fullfile(pathname,filename2);

                gGBnew(1, 1) = tempvalueGB;
                     
            dlmwrite(File1, gGBnew, 'delimiter', '\t');
            dlmwrite(File2, gGBfit, 'delimiter', '\t');
            
            for mm = 1:handles.range
                newcorgbfit1(mm) = gGBfit(mm, 1);                         
            end
            
            for mm = 1:handles.range-1
                newcorgb1(mm) = gGBnew(mm+1, 1);
            end
            
            
            
            figure('Name','Crosscorrelation Green Blue Y','NumberTitle','off')
            plot(delta1,newcorgb1,'oc',...
                delta,newcorgbfit1,'--c',...
                'LineWidth',2)
            if newcorgb1(1) >= newcorgbfit1(1)
                axis([0 range 0 newcorgb1(1)])
            else
                axis([0 range 0 newcorgbfit1(1)])
            end
                   
                guidata(hObject,handles);     
               
               
               
               
           end
           
           
           
           if sum(sum(R)) ~= 0  && sum(sum(G)) ~= 0 && sum(sum(B)) ~= 0
               

                       %gets dimensions of orig matrix
                   SG = size(R);

                   %calculates average of all matrix entries
                   avgR = sum(sum(R))/(SG(1)*SG(2));
                   avgG = sum(sum(G))/(SG(1)*SG(2));
                   avgB = sum(sum(B))/(SG(1)*SG(2));


                    deltaimagred = R - avgR;
                    deltaimaggreen = G - avgG;
                    deltaimagblue = B - avgB;

                    %--------------------------------------------------------------
                    % Calculating triple correlation function through bispectrum


                    %--------------------------------------------------------------
                    % Calculating Fast Fourier Transform of deltasignal

                    fftdeltaimagred = fftn(deltaimagred);
                    fftdeltaimaggreen = fftn(deltaimaggreen);
                    fftdeltaimagblue = fftn(deltaimagblue);

                    sfftdeltaimagred = fftshift(fftdeltaimagred);
                    sfftdeltaimaggreen = fftshift(fftdeltaimaggreen);
                    sfftdeltaimagblue = fftshift(fftdeltaimagblue);

                    figure('Name','Fourier Transform of RED','NumberTitle','off')
                    surfc(abs(sfftdeltaimagred))
                    
                    prompt = {'Enter starting point:'};
                    dlg_title = 'Input for calculating bispectrum';
                    num_lines = 1;
                    def = {'64'};
                    lowlim = inputdlg(prompt,dlg_title,num_lines,def);
                    lowlim = str2double(lowlim);

                    highlim = SG(1) - lowlim;

                    lim = highlim - lowlim;

                    nhlf = SG(1)/2;
                    nhlfp = nhlf+1;
                    nhlfm = nhlf-1;

                    nbi = lim;
                    nbihlfp = nbi/2+1;

                    r1 = zeros(lim, lim, lim, lim);

                    tic

                        for v1 = (-nhlf+lowlim):0
                            for u1 = (-nhlf+lowlim)-(v1-1):(nhlfm-lowlim)
                                for v2 = (-nhlf+lowlim):(nhlfm-lowlim)
                                    for u2 = (-nhlf+lowlim):(nhlfm-lowlim)
                                        if abs(u2+v2) <= nhlfm

                                            r1(nbihlfp + v1, nbihlfp + u1, nbihlfp + v2, nbihlfp + u2) = sfftdeltaimagred(nhlfp + u1, nhlfp + u2).*sfftdeltaimaggreen(nhlfp + v1, nhlfp + v2).*conj(sfftdeltaimagblue(nhlfp + u1 + v1, nhlfp + u2 + v2))./(SG(1)*SG(2));

                                        end
                                    end
                                end
                            end
                        end





                        for v1 = 1:(nhlfm-lowlim)
                            for u1 = (-nhlf+lowlim):(nhlfm-lowlim)-v1
                                for v2 = (-nhlf+lowlim):(nhlfm-lowlim)
                                    for u2 = (-nhlf+lowlim):(nhlfm-lowlim)
                                        if abs(u2+v2) <= nhlfm

                                            r1(nbihlfp + v1, nbihlfp + u1, nbihlfp + v2, nbihlfp + u2) = sfftdeltaimagred(nhlfp + u1, nhlfp + u2).*sfftdeltaimaggreen(nhlfp + v1, nhlfp + v2).*conj(sfftdeltaimagblue(nhlfp + u1 + v1, nhlfp + u2 + v2))./(SG(1)*SG(2));

                                        end
                                    end
                                end
                            end
                        end
                        toc


                        figure('Name','Bispectrum','NumberTitle','off')

                        colormap hsv


                        bispectdisp = abs(r1(:, :, nbihlfp, nbihlfp));
                        surfc(bispectdisp)
                        

            % End of calculating bispectrum
            %----------------------------------------------------------------------



            %----------------------------------------------------------------------
            % Calculating triple correlation function


            bispectorig = fftshift(r1);   

            tricorr = ifftn(bispectorig).*((lim^4)/(SG(1)^2*SG(2)^2));   %compute the triple correlation (inverse FFT of bispectrum)

            tricorrnorm = tricorr/(avgR*avgG*avgB);

            figure('Name','Triple Correlation Function 3D','NumberTitle','off')
            tricorrdisp = fftshift(abs(tricorrnorm(:,:,1, 1)));
            surfc(tricorrdisp)
            colormap hsv
            

                    prompt = {'Input G0:','Input w:', 'Input Ginf:', 'Input fitting range:', 'Input number of iterations:'};
                    dlg_title = 'Parameters for fitting';
                    num_lines = 1;
                    def = {'50','10', '0', '15', '30'};
                    parforfit = str2double(inputdlg(prompt,dlg_title,num_lines,def));
                    handles.g0 = parforfit(1);
                    handles.w = parforfit(2);
                    handles.ginf = parforfit(3);
                    range = parforfit(4);
                    handles.niter = parforfit(5);
                    

                    
            
            
            
            
            
            

            for ii = 1:range
                for jj = 1:range

                    testmatrix1(ii, jj) = real(tricorrnorm(ii, jj, 1, 1));
                    testmatrix2(ii, jj) = real(tricorrnorm(1, ii, jj, 1));
                    testmatrix3(ii, jj) = real(tricorrnorm(1, 1, ii, jj));
                    testmatrix4(ii, jj) = real(tricorrnorm(1, ii, 1, jj));
                    testmatrix5(ii, jj) = real(tricorrnorm(ii, 1, jj, 1));
                    testmatrix6(ii, jj) = real(tricorrnorm(ii, 1, 1, jj));

                end
            end



            for mm = 1:range

                 newtricorre1(mm) = testmatrix1(1, mm);
                 newtricorre2(mm) = testmatrix1(mm, 1);
                 newtricorre3(mm) = testmatrix1(mm, mm);

                 newtricorre4(mm) = testmatrix2(1, mm);
                 newtricorre5(mm) = testmatrix2(mm, 1);

                 newtricorre6(mm) = testmatrix3(1, mm);
                 newtricorre7(mm) = testmatrix3(mm, 1);
                 newtricorre8(mm) = testmatrix3(mm, mm);

                 newtricorre9(mm) = testmatrix4(1, mm);
                 newtricorre10(mm) = testmatrix4(mm, 1);

                 newtricorre11(mm) = testmatrix5(1, mm);
                 newtricorre12(mm) = testmatrix5(mm, 1);

                 newtricorre13(mm) = testmatrix6(1, mm);
                 newtricorre14(mm) = testmatrix6(mm, 1);

            end

            

            newt = ((newtricorre1+newtricorre2+newtricorre3+newtricorre4+newtricorre5+newtricorre6+newtricorre7+newtricorre8+newtricorre9+newtricorre10+newtricorre11+newtricorre12+newtricorre13+newtricorre14)/14)';



            % End of calculating triple correlation function
            %----------------------------------------------------------------------


        % End of calculating triple correlation function through bispectrum
        %--------------------------------------------------------------------------
                    
                    
        
        
        
        
                    correctionw = SG(1)/lim;
                    delta = [0:range-1]; 
                    TripleGinitialRGB = [handles.g0, handles.w, handles.ginf];
                    lb = [0, 0, -1000];
                    ub = [10000000, 100000000, 1000];

                    options = optimset('outputfcn',@outfun1, 'TolFun',1e-50, 'TolX', 1e-50, 'MaxFunEvals', 1000000, 'MaxIter', handles.niter, 'LevenbergMarquardt', 'on');
                    TripleGfitRGB = lsqcurvefit(@Gausshalf, TripleGinitialRGB, delta, newt, lb, ub, options);

                    TripleRGBfit = Gausshalf(TripleGfitRGB, delta);
                    
                    


                    pathname = handles.filename;
                    filename1 = 'TripleCrgb.txt';
                    filename2 = 'TripleCrgbFit.txt';
                    File1 = fullfile(pathname,filename1);
                    File2 = fullfile(pathname,filename2);



                    dlmwrite(File1, newt, 'delimiter', '\t');
                    dlmwrite(File2, TripleRGBfit, 'delimiter', '\t');


                    figure('Name','Triple Correlation Function','NumberTitle','off')
                    plot(delta,newt,'ok',...
                        delta,TripleRGBfit,'--k',...
                        'LineWidth',2)


                    guidata(hObject,handles);     
               
           end
                
%--------------------------------------------------------------------------
%Saving fitting parameters into a file



       Title1 = ['parameters:        '];
       Title2 = ['G(0)       '];
       Title3 = ['w       '];
       Title4 = ['Ginf'];
        
        Title = cat(2, Title1, Title2, Title3, Title4);
        
        fname = cat(2, handles.filename, '.txt');
        
        empty1= [' '];
        head1 = ['RED                '];
        head2 = ['GREEN              '];
        head3 = ['BLUE               '];
        head4 = ['RED-GREEN          '];
        head5 = ['RED-BLUE           '];
        head6 = ['GREEN-BLUE         '];
        head7 = ['RED-GREEN-BLUE     '];
        
        red = cat(2, head1, num2str(AutoGfitR, '%-10.5f'));
        green = cat(2, head2, num2str(AutoGfitG, '%-10.5f'));
        blue = cat(2, head3, num2str(AutoGfitB, '%-10.5f'));
        redgreen = cat(2, head4, num2str(CrossGfitRG, '%-10.5f'));
        redblue = cat(2, head5, num2str(CrossGfitRB, '%-10.5f'));
        greenblue = cat(2, head6, num2str(CrossGfitGB, '%-10.5f'));
        redgreenblue = cat(2, head7, num2str(TripleGfitRGB, '%-10.5f'));
        
        File = fullfile(handles.filename,fname);
        dlmwrite(File, Title, '');
        dlmwrite(File, empty1, '-append', 'delimiter', '');
        
        dlmwrite(File, red, '-append', 'delimiter', '');
        dlmwrite(File, green, '-append', 'delimiter', '');
        dlmwrite(File, blue, '-append', 'delimiter', '');
        dlmwrite(File, redgreen, '-append', 'delimiter', '');
        dlmwrite(File, redblue, '-append', 'delimiter', '');
        dlmwrite(File, greenblue, '-append', 'delimiter', '');
        dlmwrite(File, redgreenblue, '-append', 'delimiter', '');
                
        
        
        
        guidata(hObject, handles)
        
        
%End saving fitting parameters into a file
%--------------------------------------------------------------------------


    case 'Coincidence analysis' % User selection
    
        
        imag = imread('RGBtemp.bmp');
           
           
           R = double(imag(:, :, 1));
           G = double(imag(:, :, 2));
           B = double(imag(:, :, 3));
        
        SG = size(R);
                
        redsum = sum(sum(R));
        greensum = sum(sum(G));
        bluesum = sum(sum(B));
        
        
        RGBprod = R.*G.*B;
        
        RGprod = R.*G;
        RBprod = R.*B;
        GBprod = G.*B;
        
        numeratorRGB = sum(sum(RGBprod))*(SG(1)*SG(2))*(SG(1)*SG(2));
        denominatorRGB = redsum*greensum*bluesum;
        K3 = numeratorRGB/denominatorRGB
        
        
        numeratorRG = sum(sum(RGprod))*(SG(1)*SG(2));
        denominatorRG = redsum*greensum;
        KRG = numeratorRG/denominatorRG;
        Grg = KRG - 1
        
        
        numeratorRB = sum(sum(RBprod))*(SG(1)*SG(2));
        denominatorRB = redsum*bluesum;
        KRB = numeratorRB/denominatorRB;
        Grb = KRB - 1
        
        
        numeratorGB = sum(sum(GBprod))*(SG(1)*SG(2));
        denominatorGB = greensum*bluesum;
        KGB = numeratorGB/denominatorGB;
        Ggb = KGB - 1
        
        
        
        Grgb = K3 - 1 - Ggb - Grb - Grg
        
        
    
    
end  
            
       guidata(hObject,handles);      
            
            
    
            
            
           
           


                     
   
function stop = outfun1(x,optimValues,state)

stop = false;
 
   switch state
       case 'init'
       %    hold on
       case 'iter'
           
           
           handles = guidata(gcbo);
           
           curr_G0 = round(x(1)*100)/100;
           curr_w = round(x(2)*100)/100;
           curr_ginf = round(x(3)*10)/10;
           funvalue = optimValues.residual;
           funvaluer = round(funvalue*10)/10;
           currentiter = optimValues.iteration - 1;
           
           pause (0.1);
           
           set(handles.g0fit, 'String', curr_G0);
           set(handles.wfit, 'String', curr_w);
           set(handles.ginffit, 'String', curr_ginf);
           set(handles.resnorm, 'String', funvaluer);
           
           
          
           guidata(gcbo,handles);
           pause(0.1);
       case 'interrupt'
           
           handles = guidata(gcbo);
           stop = handles.optimstop;
           
                  
       case 'done'
           
       %    hold off
       
       otherwise
   end
                     




function range_Callback(hObject, eventdata, handles)
% hObject    handle to range (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of range as text
%        str2double(get(hObject,'String')) returns contents of range as a double


range = str2double(get(hObject,'string'));

            if isnan(range)
                errordlg('You must enter a numeric value','Bad Input','modal')
            end

    handles.range = range;
    
    guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function range_CreateFcn(hObject, eventdata, handles)
% hObject    handle to range (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end





function niter_Callback(hObject, eventdata, handles)
% hObject    handle to niter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of niter as text
%        str2double(get(hObject,'String')) returns contents of niter as a double



niter = str2double(get(hObject,'string'));

            if isnan(niter)
                errordlg('You must enter a numeric value','Bad Input','modal')
            end

    handles.niter = niter;
    
    guidata(hObject,handles);




% --- Executes during object creation, after setting all properties.
function niter_CreateFcn(hObject, eventdata, handles)
% hObject    handle to niter (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes on button press in pushtostop.
function pushtostop_Callback(hObject, eventdata, handles)
% hObject    handle to pushtostop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

handles.optimstop = true;
guidata(hObject, handles);





% --------------------------------------------------------------------
function open_Callback(hObject, eventdata, handles)
% hObject    handle to open (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

[filename, pathname] = uigetfile( ...
   {'*.bmp', 'All BMP-Files (*.bmp)'; ...
        '*.*','All Files (*.*)'}, ...
    'OPEN');

[pathstr, name, ext, versn] = fileparts(filename);

handles.filename = name;
% If "Cancel" is selected then return

if isequal([filename, pathname], [0,0])
    return
    
% Otherwise construct the fullfilename and load the file

elseif  strcmpi(ext, '.bmp')
        File = fullfile(pathname,filename);
    
    RGB = imread(File);
    si = size(RGB);
    emptymatrix = zeros(si(1), si(2));
    
    set(gcf,'CurrentAxes',handles.rgb);
        RedGreenBlue = cat(3, RGB(:, :, 1), RGB(:, :, 2), RGB(:, :, 3));
        imwrite(RedGreenBlue, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.g)
        Green = cat(3, emptymatrix, RGB(:, :, 2), emptymatrix);
        imwrite(Green, 'Greentemp.bmp');
        image(imread ('Greentemp.bmp'));
        axis off


        set(gcf,'CurrentAxes',handles.b)
        Blue = cat(3, emptymatrix, emptymatrix, RGB(:, :, 3));
        imwrite(Blue, 'Bluetemp.bmp');
        image(imread ('Bluetemp.bmp'));
        axis off
        
        
        set(gcf,'CurrentAxes',handles.r)
        Red = cat(3, RGB(:, :, 1), emptymatrix, emptymatrix);
        imwrite(Red, 'Redtemp.bmp');
        image(imread ('Redtemp.bmp'));
        axis off
   
    
   
    
     

    
else

errordlg('The program does not support this file format','File Error');

end
guidata(hObject,handles);






% --------------------------------------------------------------------
function save_Callback(hObject, eventdata, handles)
% hObject    handle to menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% Allow the user to select the file name to save to
    [filename, pathname] = uiputfile( ...
        {'*.bmp';'*.*'}, ...
        'Save as');
    % If 'Cancel' was selected then return
    if isequal([filename,pathname],[0,0])
        return
    else
        % Construct the full path and save
        File = fullfile(pathname,filename);
        
        
        
        tempimage = imread ('RGBtemp.bmp');
        imwrite (tempimage, File)
        
    end

guidata(hObject,handles);

% --------------------------------------------------------------------
function menu_Callback(hObject, eventdata, handles)
% hObject    handle to menu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)




% --------------------------------------------------------------------
function Untitled_3_Callback(hObject, eventdata, handles)
% hObject    handle to open (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function open_green_Callback(hObject, eventdata, handles)
% hObject    handle to save (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)




% --------------------------------------------------------------------
function open_red_green_blue_Callback(hObject, eventdata, handles)
% hObject    handle to open_red_green_blue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


[filename, pathname] = uigetfile( ...
   {'*.bmp', 'All BMP-Files (*.bmp)'; ...
        '*.tif', 'All TIF-Files (*.tif)'; ...
        '*.tiff', 'All TIFF-Files (*.tiff)'; ...
        '*.jpg', 'All JPG-Files (*.jpg)'; ...
        '*.jpeg', 'All JPEG-Files (*.jpeg)'; ...
        '*.*','All Files (*.*)'}, ...
    'Open Red');

[pathstr, name, ext, versn] = fileparts(filename);

handles.filename = name;


% construct the fullfilename and load the file
if isequal([filename, pathname], [0,0])
    return
    
% Otherwise construct the fullfilename and load the file

elseif  strcmpi(ext, '.bmp') | strcmpi(ext, '.tif') | strcmpi(ext, '.tiff') | strcmpi(ext, '.jpg') | strcmpi(ext, '.jpeg')
        File = fullfile(pathname,filename);
    
    R = imread(File);
    si = size(R);
    
    
    emptymatrix = zeros(si(1), si(2));
    
    
    
    set(gcf,'CurrentAxes',handles.r)
        Red = cat(3, R, emptymatrix, emptymatrix);
        imwrite(Red, 'Redtemp.bmp');
        image(imread ('Redtemp.bmp'));
        axis off
        
        
    
    set(gcf,'CurrentAxes',handles.rgb);
        RedGreenBlue = cat(3, R, emptymatrix, emptymatrix);
        imwrite(RedGreenBlue, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.g)
        image(imread ('logoMaxG.jpg'));
        axis off


        set(gcf,'CurrentAxes',handles.b)
        image(imread ('logoMaxB.jpg'));
        axis off

else

errordlg('The program does not support this file format','File Error');

        
end

[filename, pathname] = uigetfile( ...
   {'*.bmp', 'All BMP-Files (*.bmp)'; ...
        '*.tif', 'All TIF-Files (*.tif)'; ...
        '*.tiff', 'All TIFF-Files (*.tiff)'; ...
        '*.jpg', 'All JPG-Files (*.jpg)'; ...
        '*.jpeg', 'All JPEG-Files (*.jpeg)'; ...
        '*.*','All Files (*.*)'}, ...
    'Open Green');

[pathstr, name, ext, versn] = fileparts(filename);

handles.filename = name;


if isequal([filename, pathname], [0,0])
    return
    
% Otherwise construct the fullfilename and load the file

elseif  strcmpi(ext, '.bmp') | strcmpi(ext, '.tif') | strcmpi(ext, '.tiff') | strcmpi(ext, '.jpg') | strcmpi(ext, '.jpeg')
        File = fullfile(pathname,filename);
    
    G = imread(File);
   
    
    
    set(gcf,'CurrentAxes',handles.g)
        Green = cat(3, emptymatrix, G, emptymatrix);
        imwrite(Green, 'Greentemp.bmp');
        image(imread ('Greentemp.bmp'));
        axis off
        
        
    
    set(gcf,'CurrentAxes',handles.rgb);
        RedGreenBlue = cat(3, R, G, emptymatrix);
        imwrite(RedGreenBlue, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.r)
        image(imread ('Redtemp.bmp'));
        axis off


        set(gcf,'CurrentAxes',handles.b)
        image(imread ('logoMaxB.jpg'));
        axis off
else

errordlg('The program does not support this file format','File Error');

        
end

[filename, pathname] = uigetfile( ...
   {'*.bmp', 'All BMP-Files (*.bmp)'; ...
        '*.tif', 'All TIF-Files (*.tif)'; ...
        '*.tiff', 'All TIFF-Files (*.tiff)'; ...
        '*.jpg', 'All JPG-Files (*.jpg)'; ...
        '*.jpeg', 'All JPEG-Files (*.jpeg)'; ...
        '*.*','All Files (*.*)'}, ...
    'Open Blue');

[pathstr, name, ext, versn] = fileparts(filename);

handles.filename = name;


if isequal([filename, pathname], [0,0])
    return
    
% Otherwise construct the fullfilename and load the file

elseif  strcmpi(ext, '.bmp') | strcmpi(ext, '.tif') | strcmpi(ext, '.tiff') | strcmpi(ext, '.jpg') | strcmpi(ext, '.jpeg')
        File = fullfile(pathname,filename);
    
    B = imread(File);
    
    
    
    set(gcf,'CurrentAxes',handles.b)
        Blue = cat(3, emptymatrix, emptymatrix, B);
        imwrite(Blue, 'Bluetemp.bmp');
        image(imread ('Bluetemp.bmp'));
        axis off
        
        
    
    set(gcf,'CurrentAxes',handles.rgb);
        RedGreenBlue = cat(3, R, G, B);
        imwrite(RedGreenBlue, 'RGBtemp.bmp');
        image(imread ('RGBtemp.bmp'));
        axis off;

        

        set(gcf,'CurrentAxes',handles.r)
        image(imread ('Redtemp.bmp'));
        axis off


        set(gcf,'CurrentAxes',handles.g)
        image(imread ('Greentemp.bmp'));
        axis off
        
        
else

errordlg('The program does not support this file format','File Error');

        

end

guidata(hObject,handles);

% --------------------------------------------------------------------
function open_blue_Callback(hObject, eventdata, handles)
% hObject    handle to open_blue (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


