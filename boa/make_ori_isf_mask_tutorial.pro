;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;  SIMPLE EXAMPLE OF A SCRIPT CREATING A MASK FOR BASELINES BASED ON AN INITIAL REDUCTION WITHOUT MASKING
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;

ori_mask_str = ori_isf_otf_comb_no

ori_mask_str.image = ori_isf_otf_comb_no.image*0.

mask_center = ori_mask_str.image*0.
mask_center(501:1008,399:908) = 1. 
ind_mask = where(ori_isf_otf_comb_no.image gt 1. and ori_isf_otf_comb_no.weight gt 2.5 and mask_center eq 1)      ; Selecting pixels to be masked based on emission strength and weight. Should be customized
ori_mask_str.image(ind_mask) = 1.   	    	        	    	    	    	    	    	    	  ; Making sure the central region of strong emission will be masked

ind_mask = where(ori_isf_otf_comb_no.image gt 1. and ori_isf_otf_comb_no.weight gt 20)      ; Selecting additional pixels to be masked based on emission strength and weight. Should be customized
ori_mask_str.image(ind_mask) = 1.


atv, ori_mask_str.image*ori_isf_otf_comb_no.image  	    	    	    	    	    ; Inspecting the portion of the image that will be masked 

masque_str = ori_mask_str
save, filename = work_dir+'apexdata/map_otf_fits/oria_mask_str.xdr', masque_str     	    ; Storing mask for later use with "traite_otf_map_main"
