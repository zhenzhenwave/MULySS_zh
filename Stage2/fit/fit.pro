;          fit
;
; PURPOSE:
;          spectrum fitting program
;
; KEYWORDS:
;          /quiet
;          /clean
;
; NOTE:
;          not complete; no ploting
;
; OUTPUT:
;          Determined Stellar parameters
;
; AUTHOR:
;          Yue WU; Mingyi Ding
;
; UPDATE:
;          2020/11/16
;-----------------------------------------------
pro fit, clean=clean, quiet=quiet

path    = '/home/dmy/fit/'
md      = 40 ; 多项式阶数
outpath = '/home/dmy/fit/solution/'
infile  = path+'catalog_B.csv'
outfile = path+'catalog_C.csv'

; <====  从文件中，逐行读入          
readcol, infile, index_num, desig, file_name, snrg, teffin, loggin, fehin, ra, dec, $ 
SKIPLINE = 1, DELIMITER=',' ,format='F,F,A,F,F,F,F,F,F'

nl = (size(desig))[1]
outout    = fltarr(9,nl)
; 0- 3   t         g        m         rv
; 4- 7   t_err_c   g_err_c  m_err_c   rv_err_c
; 8      snr
out_czsig = fltarr(4,nl)
index1    = intarr(nl)
index2    = intarr(nl)
snr_g     = snrg
file_path = strarr(nl)

bad_spec_num = 0
; 逐个读入光谱，并使用 ulyss 拟合
for i = 0,nl-1 do begin
   time0 = systime(1)

   file_path(i) = path + 'spectrum/' + file_name(i)
   ;/home/dmy/fit/spectrum/spec-55859-F5902_sp01-050.fits

   ; <=== 拟合开始
   if file_test(file_path(i)) eq 1 then begin

      print, strtrim(i+1,2), ' ', desig(i), ' ', file_path(i)

      ; 选取有效的 光谱波长范围 4000 ~ 7000
      sp = uly_spect_read(file_path(i), 4000, 7000,/quiet) 
      ;stop
      ;uly_spect_plot,sp

      if (size(sp))[2] ne 8 then begin
         bad_spec_num = bad_spec_num + 1
      endif else begin
         f_name = index_num(i) ; eidt here 
         res = outpath+strtrim(f_name,2)
         if file_test(res+'.res') ne 1 then begin
            ; 检查初始值是否可靠
            tg = teffin(i)
            lg = loggin(i)
            zg = fehin(i)

            if (tg lt 3100) or (tg gt 5000) then begin
               print, 'Error with Teff: ',tg
               tg = [3300., 3900., 4500.]
            endif
         
            if (lg lt -0.25) or (lg gt 5.9) then begin
               print, 'Error with logg: ',lg
               lg = [-0.2, 1., 4.]
            endif

            if (zg lt -2.5) or (zg gt 2) then begin
               print, 'Error with zg: ',zg
               zg = [-2., -0.5, 1.]
            endif

            ; 设置 TGM 内插器 
            print, teffin(i), loggin(i), fehin(i)
            cmp = uly_tgm(model_file=path+'mod/miles_tgm2.fits', tg=tg, lg=lg, zg=zg)
            ;print,cmp

            time1 = systime(1)

            ; <======  拟合大气参数 
            ulyss, sp, cmp, file=res, md=md, clean=clean, quiet=quiet, /quiet, /plot
            uly_plot_save, fig_path, /PNG

            time2 = systime(1)
            print,'ulyss:', time2 - time1
            heap_free, cmp
         endif


         ; 计算拟合结果
         if file_test(res+'.fits') eq 1 then begin
            index1(i) = 1
   
     	      sol = uly_solut_tread(res+'.res')
            outout(0,i) = exp((*(sol.cmp)[0].para)[0].value)                               ;Teff
            outout(4,i) = exp((*(sol.cmp)[0].para)[0].value)*(*(sol.cmp)[0].para)[0].error ;T_err
            outout(1,i) = (*(sol.cmp)[0].para)[1].value                                    ;logg
            outout(5,i) = (*(sol.cmp)[0].para)[1].error                                    ;logg_err
            outout(2,i) = (*(sol.cmp)[0].para)[2].value                                    ;Fe/H
            outout(6,i) = (*(sol.cmp)[0].para)[2].error                                    ;Fe/H_err

            if (sol.snr gt 0. and (finite(sol.snr,/infinity) ne 1)) then outout(8,i) = sol.snr else outout(8,i) = 9999.   ;SNR : 计算中的
               outout(3,i) = sol.losvd[0]       ;rv
               outout(7,i) = sol.e_losvd[0]     ;rv_err
               out_czsig(2,i) = sol.losvd[1]    ;sigma
               out_czsig(3,i) = sol.e_losvd[1]  ;sigma_err
               heap_free, sol

               print, 'Got parameters, with SNR : ', outout(8,i)
               print,  outout(0,i), outout(1,i), outout(2,i)
               
            endif else begin
            if file_test(res+'.res') eq 1 then file_delete, res+'.res' ;bad normalized spectrum, due to bad 1D spectrum, can not fit
         endelse
         uly_spect_free, sp
         
         ; 判断拟合结果的合理性
         if (outout(0,i) lt 6000.) and $                                       ; Teff
            (outout(1,i) gt -0.24) and (outout(1,i) lt 5.9) and $              ; Log g
            (outout(2,i) gt -2.5) and (outout(2,i) ne 1.3) and $               ; Fe_H
            (abs(outout(3,i)) lt 500.) and $                                   ; RV
            (outout(8,i) ne 9999.) and $                                       ; SNR
            (out_czsig(2,i) ne 1000.) and $                                    ; 视向速度 的 Sigma，致宽影响 
            (index1(i) eq 1) then begin                                        ; ?光谱文件有效
            index2(i) = 1

         endif
      endelse
   endif else print,'-> No valid input fits file.'
   time3 = systime(1)
   print,'Escape in :',time3 - time0,' sec'
   print, '----- ----- ----- -----'
endfor

; < === index2 0\1_list 光谱的拟合是否有效：1有效，0无效
; < === cnt int 有效的拟合结果一共有多少个
; < === tmp int_list 有效的光谱的序号
tmp = where(index2 eq 1, cnt)
print,'-> valid final out num: ', cnt, ' out of ', nl

print, '-> Bad fits file num: ', bad_spec_num


; 保存结果
if file_test(outfile) eq 1 then file_delete, outfile

openw, lun, outfile, /get_lun
; 表头
print, 'write to csv file'
table_head = ['index','lamost','RA','DEC','snr','snrg','Teff','Teff_err','logg','logg_err','Fe_H','Fe_H_err','RV','RV_err','sigma','sig_err']
printf, lun, table_head, format='(17(A,:,","))'

; 参数
for i=0, nl-1 do begin
   if index2(i) eq 1 then begin ;

      pos=strpos(file_path(i), 'spec-')
      len = strlen(file_path(i))

      printf, lun, i, desig(i), ra(i), dec(i),  outout(8,i), snr_g(i), $
              outout(0,i), outout(4,i)*sqrt(outout(8,i)), $;T ;
              outout(1,i), outout(5,i)*sqrt(outout(8,i)), $;G
              outout(2,i), outout(6,i)*sqrt(outout(8,i)), $;M
              outout(3,i), outout(7,i)*sqrt(outout(8,i)), $;RV
              out_czsig(2,i), out_czsig(3,i)*sqrt(outout(8,i)),$;Sig
              format='(1(I,:,","), 1(A,:,","), 14(F,:,","))'
              ;         No.           desig  ra,dec snr,snrg TGM RV sigma
   endif
endfor

close, lun
free_lun, lun
print, '-> Finish test'
end
