# Derivação NixOS para o compilador verso.
# Uso típico num flake:
#
#   packages.x86_64-linux.verso = pkgs.callPackage ./packaging/nix/package.nix {};
#
# Ou em configuration.nix via overlay:
#
#   nixpkgs.overlays = [
#     (final: prev: { verso = prev.callPackage ./packaging/nix/package.nix {}; })
#   ];

{ lib
, stdenv
, python3
, makeWrapper
}:

stdenv.mkDerivation rec {
  pname = "verso";
  version = "0.1.0";  # TODO: sincronizar com a tag git

  src = lib.cleanSourceWith {
    src = ../..;
    filter = path: type:
      let base = baseNameOf path;
      in !(lib.hasPrefix "__pycache__" base)
      && base != ".venv"
      && base != "dist"
      && base != "build"
      && base != "bin";
  };

  nativeBuildInputs = [ makeWrapper ];
  buildInputs = [ python3 ];

  dontBuild = true;

  installPhase = ''
    runHook preInstall

    install -d $out/lib/verso
    cp -r verso main.py $out/lib/verso/

    makeWrapper ${python3}/bin/python $out/bin/verso \
      --add-flags "$out/lib/verso/main.py"

    install -Dm644 docs/sintaxe.md \
      $out/share/doc/verso/sintaxe.md

    runHook postInstall
  '';

  meta = with lib; {
    description = "Compilador da linguagem Romântica (Linguagem Poética) para C";
    homepage = "https://github.com/lvlassis/Linguagem-Verso";
    # TODO: definir licença e adicionar arquivo LICENSE
    license = licenses.unfree;
    mainProgram = "verso";
    platforms = platforms.linux;
  };
}
