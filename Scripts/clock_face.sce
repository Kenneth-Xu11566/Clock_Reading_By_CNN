//face=clockFace();
//hHand = hourHand();
//mHand = minuteHand();

//for H=0:11
//    for M=0:59
//        H
//        M
//        fileName=sprintf("regularClock_%02d_%02d.png", H, M);
//        A=analogClock(face,hHand,mHand, H, M);
//        A=imresize(A,[320, 320],interp);
//        imwrite(uint8(A), fileName);
//     end
//end

for H=0:11
    for M=0:59
        A=zeros(320, 320, 3);
        A=A+255;
        A=uint8(A);
        H0 = int32(H)/int32(10);
        H1 = int32(H)-int32(H)/int32(10)*int32(10);
        M0 = int32(M)/int32(10);
        M1 = int32(M)-int32(M)/int32(10)*int32(10);
        PH0=selectDigiPic(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, H0);
        PH1=selectDigiPic(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, H1);
        PM0=selectDigiPic(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, M0);
        PM1=selectDigiPic(C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, M1);
        
        A(111:210,5:76,:)=PH0;
        A(111:210,75:146,:)=PH1;
        A(111:210,142:177,:)=Colon;        
        A(111:210,174:245,:)=PM0;
        A(111:210,242:313,:)=PM1;
        
        H
        M
        fileName=sprintf("digitalClock_%02d_%02d.png", H, M);
        A=imresize(A,[160, 160],'area');
        imwrite(uint8(A), fileName);
     end
end


fp = mopen("digiClock.csv", "wt");
mfprintf(fp, "imageName,hour,minute\n");
for H=0:11
    for M=0:59
        fileName=sprintf("digitalClock_%02d_%02d.png", H, M);
        mfprintf(fp, "%s,%d,%f\n",fileName, int(H), M);
    end    
end
mclose(fp);


//For resize image from 320x320 to 160x160
for H=0:11
    for M=0:59
        fileNameIn=sprintf("kidKlok_%02d_%02d.png", H, M);
        fileNameOut=sprintf("kidClock_%02d_%02d.png", H, M);
        A = imread(fileNameIn);
        A = imresize(A, [160, 160], 'area');
        imwrite(uint8(A), fileNameOut);
    end    
end

//For padding image from 160x160 to 224x224
for H=0:11
    for M=0:59
        A=zeros(224, 224, 3);
        A=A+255;
        A=uint8(A);
        fileNameIn=sprintf("digitalClock_%02d_%02d.png", H, M);
        fileNameOut=sprintf("trans_digitalClock_%02d_%02d.png", H, M);
        B = imread(fileNameIn);
        A(33:192, 33:192, :) = B;
        imwrite(uint8(A), fileNameOut);
    end
end


// Ploting 
plot2d(10:200, CC(10:200,1), 1)
plot2d(10:200, DD(10:200,1), 3)
plot2d(10:200, EE(10:200,1), 5)
legends(['Digital Clock';'Analog Clock';'KidKlok'],[1,3,5],opt="ur")
xlabel("Epoch")
ylabel("Loss")
title("Training Loss of Tranform Learning")


clf
plot2d(10:200, CC(10:200,2), 1)
plot2d(10:200, DD(10:200,2), 3)
plot2d(10:200, EE(10:200,2), 5)
legends(['Digital Clock';'Analog Clock';'KidKlok'],[1,3,5],opt="lr")
xlabel("Epoch")
ylabel("Average Absolute Neuron Ouput")
title("Average Absolute Neuron Output of Tranform Learning")

clf
plot2d(10:200, CCC(10:200,1), 1)
plot2d(10:200, DDD(10:200,1), 3)
plot2d(10:200, EEE(10:200,1), 5)
legends(['Digital Clock';'Analog Clock';'KidKlok'],[1,3,5],opt="ur")
xlabel("Epoch")
ylabel("Loss")
title("Training Loss")

clf
plot2d(10:200, CCC(10:200,2), 1)
plot2d(10:200, DDD(10:200,2), 3)
plot2d(10:200, EEE(10:200,2), 5)
legends(['Digital Clock';'Analog Clock';'KidKlok'],[1,3,5],opt="lr")
xlabel("Epoch")
ylabel("Average Absolute Neuron Ouput")
title("Average Absolute Neuron Output")

