function B=clockFace()
    B=zeros(1280,1280,3);
    centerX = 640.5;
    centerY = 640.5;
    for i=1:1280
        for j=1:1280
            r = sqrt((i-centerY)^2 + (j-centerX)^2);
            if ( r > 510 || r< 400) then
                B(i,j,1) = 210;
                B(i,j,2) = 210;
                B(i,j,3) = 210;

            else if  r >  490 || abs(i-centerY)<8 || abs(j-centerX)<8 then 
                B(i,j,1) = 10;
                B(i,j,2) = 10;
                B(i,j,3) = 10;
            else 
                B(i,j,1) = 210;
                B(i,j,2) = 210;
                B(i,j,3) = 210;
            end      
        end
    end
    end
endfunction

function B=hourHand()
    B=zeros(1280,1280,3);
    bcenterX = 640.5;
    centerY = 640.5;
    B=B+210;
    for i=280:650
        for j=631:650
                B(i,j,1) = 10;
                B(i,j,2) = 10;
                B(i,j,3) = 10;            
        end
    end
endfunction

function B=minuteHand()
    B=zeros(1280,1280,3);
    bcenterX = 640.5;
    centerY = 640.5;
    B=B+210;
    for i=200:650
        for j=631:650
                B(i,j,1) = 10;
                B(i,j,2) = 10;
                B(i,j,3) = 10;            
        end
    end
endfunction


function A=analogClock(face, hHand, mHand, hour, minute)
    A=face;
    pi = 3.141592654;
    centerX = 640.5;
    centerY = 640.5;
    hour = int32(hour);
    if hour < 0 then
        hour = 0;
    end
    if hour > 11 then
        hour = 11;
    end
    hour = double(hour);
    minute = int32(minute);
    if minute < 0 then
        minute = 0;
    end
    if minute > 59 then
        minute = 59;
    end
    minute = double(minute);
    rotationMinute = 2*pi/60*minute;
    rotationHour = 2*pi/12*hour + 2*pi/60*minute/12;
    
    for i=1:1280
        for j=1:1280
            x = j-centerX;
            y = centerY-i;
            
            //////////////// SuperImposing Minute Handle //////////
            xM = cos(rotationMinute)*x-sin(rotationMinute)*y;
            yM = sin(rotationMinute)*x+cos(rotationMinute)*y;
            jM= xM+centerX+.5;
            iM= centerY-yM+.5;
            if ( iM >= 1 && iM <= 1280 && jM >= 1 && jM <= 1280  ) then
                if ( mHand(iM, jM, 1)<15) 
                    A(i,j,1) = mHand(int32(iM), int32(jM),1);
                    A(i,j,2) = mHand(int32(iM), int32(jM),2);
                    A(i,j,3) = mHand(int32(iM), int32(jM),3);
                end
            end
            //////////////// SuperImposing Hour Handle //////////
            xH = cos(rotationHour)*x-sin(rotationHour)*y;
            yH = sin(rotationHour)*x+cos(rotationHour)*y;
            jH= xH+centerX+.5;
            iH= centerY-yH+.5;
            if ( iH >= 1 && iH <= 1280 && jH >= 1 && jH <= 1280  ) then
                if ( hHand(iH, jH, 1)<15) 
                    A(i,j,1) = hHand(int32(iH), int32(jH),1);
                    A(i,j,2) = hHand(int32(iH), int32(jH),2);
                    A(i,j,3) = hHand(int32(iH), int32(jH),3);
                end
            end
        end
    end
    
endfunction

function A=selectDigiPic(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, number)
    if number == 0 then
        A = C0;
    end
    if number == 1 then
        A = C1;
    end
    if number == 2 then
        A = C2;
    end
    if number == 3 then
        A = C3;
    end
    if number == 4 then
        A = C4;
    end
    if number == 5 then
        A = C5;
    end
    if number == 6 then
        A = C6;
    end
    if number == 7 then
        A = C7;
    end
    if number == 8 then
        A = C8;
    end
    if number == 9 then
        A = C9;
    end
endfunction

