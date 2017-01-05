## XALT: Getting details for a given User ID (CSCS DB)

* Go to [http://tpc14.cscs.ch/xalt-portal.git/xaltindex.html](http://tpc14.cscs.ch/xalt-portal.git/xaltindex.html)
and enter a `UserID` (syshost and dates are ignored) 

<img src="img/xalt_cscs_startpage.png" alt="xalt_cscs_startpage" >

---
### Groups and Executables
* Clicking on the submit button will show the list of `groups` for the given userid
plus the list of `executables` run by the same userid on Daint:

<img src="img/xalt_cscs_listgid_listexes.png" alt="xalt_cscs_listgid_listexes" >

---
### Project details
* Selecting one of the row in the first table will display more details for the
selected project id
    * for instance for project `s715`:
<img src="img/xalt_cscs_pi+usage_gids715.png" alt="gids715" height="200px" >

    * and for project `u1`:
<img src="img/xalt_cscs_pi+usage_gidu1.png" alt="gidu1" height="200px" >

---
### Troubleshooting
* If a user did not use its allocation, then a table may be empty:
<img src="img/xalt_cscs_pi+usage_gids663.png" alt="gids663" height="200px" >

    * as confirmed by `sbucheck`:
<img src="img/xalt_cscs_pi+usage_gids663_zero.png" alt="gids663_zero" >

