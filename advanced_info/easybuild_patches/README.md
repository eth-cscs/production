# Set up source tree and generate patch file

Untar the source package and make a backup copy (for being able to 'diff')

<pre>
tar xf source.tar.bz2 ; cp -r source/ source.orig/
</pre>  

Apply the needed corrections to the files under source/

The EasyBuild-compatible patch file is generated as

<pre>
diff -Nru source.orig source/ > patch_file.patch
</pre>

The diff command must be executed at least at the top of the package source tree (or anywhere outside the package itself), so that the full source tree could appear within the .patch file. This last condition is required by EasyBuild in order to correctly define the patch level within the source tree. 

## Diff against non-existing file

If you are adding only one new file, patch might not automatically find the patch level. In that case you can use:

<pre>
patches = [('new.file', 'dest/path/')]
</pre>

---

# Install the patch

Create the easyconf file (patch_easyconf.eb) according to instructions in [source files and patches section](http://easybuild.readthedocs.io/en/latest/Writing_easyconfig_files.html#common-easyconfig-parameters) adding the patch file name, with relative path with respect to the easyconf file position. The easyconf file shall therefore include the patch line

<pre>
patches = ['relative_path/patch_file.patch'] 
</pre>

Run EasyBuild module installation

<pre>
eb &ltoptions&gt patch_easyconf.eb
</pre>

If the patch is applied on an already installed module, the above command must be modified in order to force the installation of the patched module. In this case the command is 

<pre>
eb &ltoptions&gt patch_easyconf.eb -f
</pre>