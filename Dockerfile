FROM quay.io/biocontainers/minvar:2.2--py36_0
COPY --from=mdoering88/bamtofreq:latest bamToFreq/bin/bamToFreq /usr/bin/
COPY run_minvar.sh /usr/bin/
COPY cli.py /usr/local/lib/python3.6/site-packages/minvar/
ENTRYPOINT ["run_minvar.sh"]
CMD []
