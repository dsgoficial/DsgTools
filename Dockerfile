FROM qgis/qgis:release-4_0
RUN mkdir /tests_directory && \
    qgis_setup.sh DsgTools && \
    cd /tests_directory && \
    git clone --progress --verbose https://github.com/dsgoficial/DsgTools.git && \
    rm -f  /root/.local/share/QGIS/QGIS4/profiles/default/python/plugins/DsgTools && \
    ln -s /tests_directory/DsgTools/ /root/.local/share/QGIS/QGIS4/profiles/default/python/plugins/DsgTools

ENV PYTHONPATH=/usr/share/qgis/python/:/usr/lib/python3/dist-packages/qgis:/usr/share/qgis/python/qgis:/usr/share/qgis/python/qgis/python/:/usr/share/qgis/python/qgis/python/plugins/:/root/.local/share/QGIS/QGIS4/profiles/default/:/root/.local/share/QGIS/QGIS4/profiles/default/python/:/root/.local/share/QGIS/QGIS4/profiles/default/python/plugins/:/root/.local/share/QGIS/QGIS4/profiles/default/python/plugins/DsgTools
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
