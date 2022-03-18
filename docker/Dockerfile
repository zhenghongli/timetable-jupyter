FROM nvcr.io/nvidia/tensorflow:21.04-tf2-py3
RUN pip install --upgrade jupyterlab jupyterlab-git
RUN apt-get update
RUN apt-get install sudo -y
RUN apt-get install -y npm nodejs
RUN python3 -m pip install --no-cache --upgrade setuptools pip
ENV JUPYTER_USER=joyvan
ENV JUPYTER_PASSWORD=joyvan
RUN useradd -ms /bin/bash $JUPYTER_USER -G sudo
RUN echo "${JUPYTER_USER}:${JUPYTER_PASSWORD}" | chpasswd
ADD run.sh /opt/run.sh
RUN chown $JUPYTER_USER:$JUPYTER_USER /opt/run.sh
RUN chmod 777 /opt/run.sh
ADD security.py /opt/security.py
RUN chown $JUPYTER_USER:$JUPYTER_USER /opt/security.py
RUN chmod 777 /opt/security.py

USER $JUPYTER_USER
WORKDIR /home/$JUPYTER_USER
RUN mkdir notebook
CMD /opt/run.sh

