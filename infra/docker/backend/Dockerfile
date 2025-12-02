FROM swippter-backend-dependencies:latest
RUN source .venv/bin/activate
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/swippter
EXPOSE 8000
COPY infra/docker/backend/server/entrypoint.sh /app/swippter/entrypoint.sh
RUN chmod +x /app/swippter/entrypoint.sh
ENTRYPOINT ["/app/swippter/entrypoint.sh"]