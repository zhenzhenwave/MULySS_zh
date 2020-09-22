;          fit_b16
;
; PURPOSE:
;          comp b16
;
; KEYWORDS:
;          /quiet
;          /clean
;
; NOTE:
;          '*****' places need manually set
;
; OUTPUT:
;          Determined parameters
;
; AUTHOR:
;          Yue WU
;
; UPDATE:
;          2018/01/18
;-----------------------------------------------
pro fit_b16_1, clean=clean, quiet=quiet

path    = '/usr/local/ulyss/pgm/indep/'
md      = 15 ;*****
outpath = '/usr/local/ulyss/pgm/indep/res_nc_b16_1/'
infile  = path+'table_b16_modified'
outfile = path+'table_b16_out_1'
my_file = path+'files/DataBase_b16.txt'

; <====  从文件中读入
readcol, infile, designation, spt, teffin, zeta, fehin, veloin,format='A,F,F,F,F,F'
nl = (size(designation))[1]
;delete the * tail
for i=0,nl-1 do begin

   designation(i)= strmid(designation(i),0,19)

endfor

outout    = fltarr(9,nl)
; 0- 3   t         g        m         rv
; 4- 7   t_err_c   g_err_c  m_err_c   rv_err_c
; 8      snr
out_czsig = fltarr(4,nl)
index1    = intarr(nl)
index2    = intarr(nl)

; Loop: extract specpath and call ulyss to fit
bad_spec_num = 0
spec_path = strarr(nl)
snr_r = fltarr(nl)
; < == 打开文件（模拟DataBase检索结果）
openr, lun, my_file , /get_lun

for i = 0,nl-1 do begin
   time0 = systime(1)
   ;openmysql_pp, lun, 'dr2',host='172.17.0.12',user='lamost_uly',pass='lamost_uly_zf', error, /silent
   ;openmysql_pp,lun,Getenv('MYSQLNAME_DR2'),error, /silent
   ;cmd = 'select specpath,snrr from dr2_spec_final where designation="'+string(designation(i))+'";'
   ;mysqlquery, lun, cmd, specpath, snrr, format='a,f'
   str_tmp = ''
   readf, lun, str_tmp
   DESIG_name = strmid(str_tmp,0,19)
   snrr = strmid(str_tmp,20,5)
   specpath = strmid(str_tmp,26)

   ; < ===  specpath 是文件绝对地址
   ; spec_path(i)= '/home/wuyue/data7/'+strmid(specpath,7,len-7)
   spec_path(i) = path + 'files/' + specpath
   ;/usr/local/ulyss/pgm/indep/files/spec-55859-F5902_sp01-050.fits

   snr_r(i)= snrr
   ;out_czsig = fltarr(4)


   ; < === 得知文件路径了， 对该fits文件进行光谱分析
   if file_test(spec_path(i)) eq 1 then begin

      print, strtrim(i+1,2), ' ', designation(i), ' ', spec_path(i)
      ; < === 修改了, uly_spect_read_lms 但并未找到
      sp = uly_spect_read(spec_path(i), 4000, 7300,/quiet)
      ;stop
      ;uly_spect_plot,sp
      if (size(sp))[2] ne 8 then begin
         bad_spec_num = bad_spec_num + 1
      endif else begin
         pos = strpos(spec_path(i), 'spec-')
         len = strlen(spec_path(i))
         f_name = strmid(spec_path(i), pos, len-pos-5)

         res = outpath+strtrim(f_name,2)
         if file_test(res+'.res') ne 1 then begin
            ;check if cfi_param outside ulyss valid scope
            ;if (db1 gt 3100) and (db1 lt 40000) and $
             ;  (db2 gt -0.25) and (db2 lt 5.9) and $
             ;  (db3 gt -2.5) and (db3 lt 1.0) then begin
             ;  cmp = uly_tgm(tg=db1,lg=db2,zg=db3)
 ;          print,cmp
            ;endif el:se begin
            cmp = uly_tgm(model_file=path+'mod/miles_tgm2.fits',tg=teffin(i),lg=[2.,4.],zg=fehin(i))
            ;endelse
 ;           print,cmp
            time1 = systime(1)
            ulyss, sp, cmp, file=res, md=md, clean=clean, quiet=quiet;, /plot
            ;stop
            time2 = systime(1)
            print,'ulyss:', time2 - time1
            heap_free, cmp
         endif
         if file_test(res+'.fits') eq 1 then begin
            index1(i) = 1
            ;stop
     	    sol = uly_solut_tread(res+'.res')
            outout(0,i) = exp((*(sol.cmp)[0].para)[0].value)                               ;Teff
            outout(4,i) = exp((*(sol.cmp)[0].para)[0].value)*(*(sol.cmp)[0].para)[0].error ;T_err
            outout(1,i) = (*(sol.cmp)[0].para)[1].value                                    ; logg
            outout(5,i) = (*(sol.cmp)[0].para)[1].error                                    ;logg_err
            outout(2,i) = (*(sol.cmp)[0].para)[2].value                                    ;Fe/H
            outout(6,i) = (*(sol.cmp)[0].para)[2].error                                    ;Fe/H_err
            if (sol.snr gt 0. and (finite(sol.snr,/infinity) ne 1)) then outout(8,i) = sol.snr else outout(8,i) = 9999.
            outout(3,i) = sol.losvd[0]     ;rv
            outout(7,i) = sol.e_losvd[0]   ;rv_err
            out_czsig(2,i) = sol.losvd[1]  ;sigma
            out_czsig(3,i) = sol.e_losvd[1];sigma_err
            heap_free, sol
         endif else begin
            if file_test(res+'.res') eq 1 then file_delete, res+'.res' ;bad normalized spectrum, due to bad 1D spectrum, can not fit
         endelse

         uly_spect_free, sp

         flag_cut = intarr(1)
         flag_cut = (outout(0,i) gt 10000. and outout(2,i) lt -0.5)
         if outout(0,i) lt 20000. and $
            outout(1,i) gt -0.24 and outout(1,i) lt 4.9 and $
            outout(2,i) gt -2.50 and outout(2,i) ne 1.00 and $
            abs(outout(3,i)) lt 500. and $
            flag_cut ne 1 and $
            outout(8,i) ne 9999. and $
            out_czsig(2,i) ne 1000. and $
            index1(i) eq 1 then begin


            index2(i) = 1

         endif
         ;stop

      endelse

   endif else print,'-> No valid input fits file.'
   time3 = systime(1)
   print,time3 - time0
endfor


; < === 释放逻辑设备号
free_lun, lun


tmp = where(index2 eq 1, cnt)
print,'-> valid final out num: ', cnt, 'out of ', nl

print, '-> Bad fits file num: ', bad_spec_num


;save output
if file_test(outfile) eq 1 then file_delete, outfile
openw, lun, outfile, /get_lun
for i=0, nl-1 do begin

   if index2(i) eq 1 then begin ;?????*****

      pos=strpos(spec_path(i), 'spec-')
      len = strlen(spec_path(i))
      f_name = strmid(spec_path(i), pos, len-pos-5)
      ;stop
;      printf, lun, i+1, designation(i), f_name, snr_r(i), outout(8,i), $
;             outout(0,i), outout(4,i), outout(4,i)*sqrt(outout(8,i)), $;T ;?????
;            outout(1,i), outout(5,i), outout(5,i)*sqrt(outout(8,i)), $;G
;           outout(2,i), outout(6,i), outout(6,i)*sqrt(outout(8,i)), $;M
;              outout(3,i), outout(7,i), outout(7,i)*sqrt(outout(8,i)), $;RV
;             out_czsig(2,i), out_czsig(3,i), out_czsig(3,i)*sqrt(outout(8,i)),$;Sig
;         format='(1I-5, 1A-21, 1A-42, 2F7.2, 3F9.1, 3F8.2, 3F9.2, 3F8.1, 3F8.1)'
              ;        No.  desig   name  snrr snr   T     G      M      RV   sigma


      printf, lun, i+1, designation(i), f_name, snr_r(i), outout(8,i), $
              outout(0,i), outout(4,i)*sqrt(outout(8,i)), $;T ;?????
              outout(1,i), outout(5,i)*sqrt(outout(8,i)), $;G
              outout(2,i), outout(6,i)*sqrt(outout(8,i)), $;M
              outout(3,i), outout(7,i)*sqrt(outout(8,i)), $;RV
              out_czsig(2,i), out_czsig(3,i)*sqrt(outout(8,i)),$;Sig
              format='(1I-5, 1A-21, 1A-42, 2F7.2, 2F9.1, 2F8.2, 2F9.2, 2F8.1, 2F8.1)'
              ;        No.  desig   name  snrr snr   T     G      M      RV   sigma






   endif

endfor
close, lun
free_lun, lun

;plot figure
;plot distribution figures of dr12 parameters
if !d.name ne 'PS' then device, decomposed = 0
white = fsc_color('White')
grey  = fsc_color('Grey')
blue  = fsc_color('Blue');Violet Cyan Orange
black = fsc_color('Black')
green = fsc_color('Green')
red   = fsc_color('Red')
violet= fsc_color('Violet')
cyan  = fsc_color('Cyan')
orange= fsc_color('Orange')
charsize= 1.6;1.5 ;3.2
charthick=1.5 ;0.9
psym=3        ;1->+, 6->square
symsize= 2.  ;0.8
xstyle=1
ystyle=1
thick=2  ;4
xthick=2 ;4
ythick=2 ;4
linestyle = 0 ;line style for gaussian

xr1=[max(outout(0,tmp))+0.5,min(outout(0,tmp))-0.5]
yr1=[min(outout(1,tmp))-0.5,max(outout(1,tmp))+0.5]

;== plot teff vs logg ==
plot,alog10(outout(0,tmp)),outout(1,tmp), xtitle='log(Teff)', $
	xr=xr1,xstyle=xstyle, xthick=xthick, ytickin=1, xtickin=0.1, $
      xmargin=[12,2], yr=yr1, ythick=ythick, ystyle=ystyle, ymargin=[3.5,1], $
      xticklen=0.025, yticklen=0.015, charsize=charsize, ytitle='log g', $
      charthick=charthick, /nodata, thick=thick, xminor=2, yminor=2, BACKGROUND = grey
oplot, alog10(outout(0,tmp)),outout(1,tmp), psym=psym, symsize=symsize, color= black
;oplot, (alog10(para(3,*)))(tm3), (para(5,*))(tm3), psym=psym, symsize=symsize, color= blue
;< === 注释了stop
;stop

;== plot teff vs feh ==
xr1=[max(outout(0,tmp))+0.5,min(outout(0,tmp))-0.5]
yr1=[min(outout(2,tmp))-0.5,max(outout(2,tmp))]+0.5
plot,alog10(outout(0,tmp)),outout(2,tmp), xtitle='log(Teff)', $
        xr=xr1,xstyle=xstyle, xthick=xthick, ytickin=1, xtickin=0.1, $
      xmargin=[12,2], yr=yr1, ythick=ythick, ystyle=ystyle, ymargin=[3.5,1], $
      xticklen=0.025, yticklen=0.015, charsize=charsize, ytitle='feh', $
      charthick=charthick, /nodata, thick=thick, xminor=2, yminor=2, BACKGROUND = grey
oplot, alog10(outout(0,tmp)),outout(2,tmp), psym=psym, symsize=symsize, color= black
;stop


;== plot check teff ==
plot, teffin(tmp), outout(0,tmp),psym=psym, symsize=symsize, color= black
;stop


;== plot check feh ==
plot,fehin(tmp), outout(2,tmp),psym=psym, symsize=symsize, color= black
;stop
;ok

;'== plot check rv ==
tmp1 = where(index2 eq 1 and veloin ne -9999, cnt1)
plot, veloin(tmp1), outout(3,tmp1),psym=psym, symsize=symsize, color= black
;stop


print, '-> Finish fit_b16_1'

end
;=========================
