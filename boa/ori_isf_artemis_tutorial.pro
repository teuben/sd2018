;
@obs1_artemis_config	; Configuring directories/project name/calibration files. -  File obs1_artemis_config.pro to be customized depending on your local installation (e.g. project name and location of rawdata, calibration files)

print, work_dir     	; ArTeMiS root directory.  Rawdata in IDL format will be stored in work_dir+'apexdata/basic_xdr/350' and work_dir+'apexdata/basic_xdr/450' at 350 and 450 microns, respectively
    	    	    	;   	    	    	   Reduced data in IDL format will be stored in work_dir+'apexdata/map_otf_xdr/project_name/350' and work_dir+'apexdata/map_otf_xdr/project_name/450'

;
;;;build_apexobslog, apex_log		    	    	; Collects available observing logs and stores in apex_obslog.xdr
;
;apexdata=work_dir+'apexdata/'
;restore, apexdata+'obslogs/apex_obslog.xdr', /verb
;
;;;; Selecting and displaying information on OTF scans observed on Ori-ISF
;
;id_otf_isf = where(strmid(apexlog_struct.source,0,7) eq 'Ori-ISF' and apexlog_struct.type eq 'MAP' and apexlog_struct.type eq 'MAP' and apexlog_struct.mode eq 'OTF' and apexlog_struct.totalscantime gt 60., otf_map_count)
;
;for i = 0, otf_map_count-1 do begin $
;& raw_files = findfile(apexdata+'rawdata/*'+strtrim(string(apexlog_struct(id_otf_isf(i)).number),1)+'*', count=n_files) $
;& n_raw(i) = n_files $
;& if n_files ge 1 then print, "Scan_number: ", apexlog_struct(id_otf_isf(i)).number, "  Source: ", apexlog_struct(id_otf_isf(i)).source, "   Observing date: ", apexlog_struct(id_otf_isf(i)).date, "   PWV (mm): ", apexlog_struct(id_otf_isf(i)).pwv & $
;endfor
;

; Examples showing how skydips can be reduced with the IDL Pipeline APIS:

;init_obs, scan_number= 77385, type = 'map', init_obs_str    	    	    	    	    	    	    ; tau350 = 0.97255804 +-      0.019868609    (PWV  = 0.56 mm)   	Result at 350 mu (default band)
noise_fft_skydip, 77385, sky_str, /nopowermap

;init_obs, scan_number= 77385, type = 'map', init_obs_str, band=450
noise_fft_skydip, 77385, sky_str, /nopowermap, band=450	    	    	    	    	    	            ; tau450 = 0.79566951 +-      0.022166610   (PWV  = 0.56 mm) 	Result at 450 mu

;

;init_obs, scan_number= 77393, type = 'map', init_obs_str    	    	    	    	    	    	    ; tau350 = 0.97449361 +-     0.0058531398   (PWV  = 0.70 mm)
noise_fft_skydip, 77393, sky_str, /nopowermap

;init_obs, scan_number= 77393, type = 'map', init_obs_str, band=450
noise_fft_skydip, 77393, sky_str, /nopowermap, band=450	    	    	    	    	    	            ; tau450 = 0.81118928 +-    0.00066667644   (PWV  = 0.70 mm)

    ;
    ; init_obs: Reads in and fills a structure containing directory path, calibration file and subscan list for a given scan. Need not be executed but useful.
    ; 

;init_obs, scan_number= 77384, type = 'map', init_obs_str    	    	    	    	   ;  The init_obs procedure may be used to check whether the raw data from a particular scan (here 77384) are available
;traite_otf_map_main, scan_number= 77384, type = 'decorrel', v883_ori_77384, tau=0.97, /newreduc

;init_obs, scan_number= 77390, type = 'map', init_obs_str
;traite_otf_map_main, scan_number= 77390, type = 'decorrel', uranus_77390, tau=0.97, /newreduc	    	    ; Reducing a calibration scan on Uranus
;atv, uranus_77390.image    	    	    	    	    	    	    	    	    	    	    ; Visualizing the resulting image
;
;
;init_obs, scan_number= 77391, type = 'map', init_obs_str
;traite_otf_map_main, scan_number= 77391, type = 'decorrel', ori_isf_otf_77391_str, tau=0.99, /newreduc

;init_obs, scan_number= 77392, type = 'map', init_obs_str
traite_otf_map_main, scan_number= 77392, type = 'decorrel', carina_77392, tau=0.99, /newreduc	    	    ; Reducing a calibration scan on Carina (taken in spiral mode)
atv, carina_77392.image     	    	    	    	    	    	    	    	    	    	    ; Visualizing the resulting image
atv, carina_77392.weight    	    	    	    	    	    	    	    	    	    	    ; Visualizing the corresponding weight map


;;;;;;
;;;;;; Examples of commands showing how big maps taken in on-the-fly (OTF) mode can be reduced with APIS.
;;;;;; Here two big scans (77389 and 77391), each consisting of 125 subscans/rows, observed toward the Orion A integral-shaped filament
;
;;;;;; First iteration: Data reduction without any masking.
;;;;;;


traite_otf_map_main, scan_number= 77389, type = 'decorrel', ori_isf_otf_77389_no_str, tau=0.97, /newreduc   ;  Reducing scan 77389, result stored in IDL structure ori_isf_otf_77389_no_str (can be given another name)
atv, ori_isf_otf_77389_no_str.image 	    	    	    	    	    	    	    	    	    ;  Visualizing the resulting image with atv
atv, ori_isf_otf_77389_no_str.weight	    	    	    	    	    	    	    	    	    ;  Visualizing the corresponding weight map


traite_otf_map_main, scan_number= 77391, type = 'decorrel', ori_isf_otf_77391_no_str, tau=0.99, /newreduc   ;  Reducing scan 77391, storing result in IDL structure ori_isf_otf_77391_no_str 

combine_otf_map, [77389,77391], ori_isf_otf_comb_no 	    	    	    	    	    	    	    ;  Combining the two scans (77389, 77391) into a single map, stored in structure ori_isf_otf_comb_no  (can be given another name)

atv, ori_isf_otf_comb_no.image	    	    	    	    	    	    	    	    	    	    ;  Visualizing the combined image with atv
atv, ori_isf_otf_comb_no.weight	    	    	    	    	    	    	    	    	    	    ;  Visualizing the weight map of the combined data

make_fits, ori_isf_otf_comb_no, fileout='ori_isf_otf_comb350_77389_77391_not_masked'	    	    	    ;  Storing the result in a fits file called ori_isf_otf_comb350_77389_77391_not_masked.fits which will be located in directory work_dir+'apexdata/map_otf_fits'

;
;;;;;; Second iteration: Data reduction with masking the regions of the map with bright emission (See script make_ori_isf_mask_tutorial.pro for an example of how the mask can be generated.)
;
;;;;;; Masked

traite_otf_map_main, scan_number= 77389, type = 'decorrel', ori_isf_otf_77389_str, champ_base='oria_herschel_mask_str.xdr', tau=0.97, /newreduc      	    	; Reducing scan 77389 at 350mu using mask 'oria_herschel_mask_str.xdr'
;;;;traite_otf_map_main, scan_number= 77389, type = 'decorrel', ori_isf_otf_77389_str, champ_base='oria_herschel_mask_str.xdr', /tau, /newreduc

make_fits, ori_isf_otf_77389_str, fileout='ori_isf_otf_77389_350'   	    	;  Storing result in fits file

traite_otf_map_main, scan_number= 77389, type = 'decorrel', ori_isf_otf_77389_450_str, champ_base='oria_herschel_mask_str.xdr', band=450, tau=0.80, /newreduc	; Reducing scan 77389 at 450mu using mask 'oria_herschel_mask_str.xdr'

;
traite_otf_map_main, scan_number= 77391, type = 'decorrel', ori_isf_otf_77391_str, champ_base='oria_herschel_mask_str.xdr', tau=0.99, /newreduc      	    	; Reducing scan 77391 at 350mu using mask 'oria_herschel_mask_str.xdr'
;;;;traite_otf_map_main, scan_number= 77391, type = 'decorrel', ori_isf_otf_77391_str, champ_base='oria_herschel_mask_str.xdr', /tau, /newreduc

make_fits, ori_isf_otf_77391_str, fileout='ori_isf_otf_77391_350'  	    	;  Storing result in fits file

traite_otf_map_main, scan_number= 77391, type = 'decorrel', ori_isf_otf_77391_450_str, champ_base='oria_herschel_mask_str.xdr', band=450, tau=0.81, /newreduc	; Reducing scan 77391 at 450mu using mask 'oria_herschel_mask_str.xdr'


combine_otf_map, [77389,77391], ori_isf_otf_comb	    	    	        ; Combining the two scans (77389, 77391) into a single map at 350mu, stored in structure ori_isf_otf_comb  (can be given another name)

make_fits, ori_isf_otf_comb, fileout='ori_isf_otf_comb350_77389_77391_masked'	; Storing result in fits file

;;;;;

combine_otf_map, [77389,77391], ori_isf_otf_comb_450, band=450	            	    ; Combining the two scans (77389, 77391) into a single map at 350mu, stored in structure ori_isf_otf_comb_450  (can be given another name)

make_fits, ori_isf_otf_comb_450, fileout='ori_isf_otf_comb450_77389_77391_masked'   ; Storing result in fits file


