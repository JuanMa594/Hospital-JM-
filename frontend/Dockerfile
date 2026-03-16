# Build stage
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copiar csproj y restaurar dependencias
COPY ["FrontEndBlazor.csproj", "./"]
RUN dotnet restore "FrontEndBlazor.csproj"

# Copiar el resto y compilar
COPY . .
RUN dotnet build "FrontEndBlazor.csproj" -c Release -o /app/build

# Publicar
FROM build AS publish
RUN dotnet publish "FrontEndBlazor.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Run stage
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .

# Variables de entorno por defecto
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
ENV BACKEND_URL=http://localhost:8000

# El puerto 8080 es usado por defecto por la imagen aspnet
EXPOSE 8080

ENTRYPOINT ["dotnet", "FrontEndBlazor.dll"]
