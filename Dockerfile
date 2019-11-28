FROM qgis/qgis:final-3_4_13
RUN mkdir /tests_directory && \
    qgis_setup.sh DsgTools && \
    cd /tests_directory && \
    git clone --progress --verbose https://github.com/dsgoficial/DsgTools.git && \
    rm -f  /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DsgTools && \
    ln -s /tests_directory/DsgTools/ /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DsgTools

ENV PYTHONPATH=/usr/share/qgis/python/:/usr/lib/python2.7/dist-packages/qgis:/usr/lib/python3/dist-packages/qgis:/usr/share/qgis/python/qgis:/root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/DsgTools
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]