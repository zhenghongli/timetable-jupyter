#!/bin/bash
#echo 'password' | sudo useradd $1
#echo 'password' | sudo -S service ssh restart

jupyter notebook --generate-config
python /opt/security.py $1
#echo "c.NotebookApp.password = $(python security.py $1)" >> ~/.jupyter/jupyter_notebook_config.py
#echo "c.NotebookApp.port = 8080"  >> /usr/local/etc/jupyter/jupyter_notebook_config.py
#echo "c.NotebookApp.notebook_dir = '$HOME'" >> /usr/local/etc/jupyter/jupyter_notebook_config.py
#echo "c.NotebookApp.allow_password_change = False"  >> /usr/local/etc/jupyter/jupyter_notebook_config.py
#echo "c.NotebookApp.token = ''"   >> /usr/local/etc/jupyter/jupyter_notebook_config.py

echo "c.NotebookApp.port = 8080"  >> $HOME/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.notebook_dir = '$HOME'" >> $HOME/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.allow_password_change = False"  >> $HOME/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.token = ''"   >> $HOME/.jupyter/jupyter_notebook_config.py
jupyter lab
