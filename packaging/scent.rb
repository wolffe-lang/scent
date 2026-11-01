# PREPARED, NOT PUBLISHED. Shape: lope bc388673 packaging/lope.rb.
# Source build from a future tag; no dependency on a moving wolf formula.
class Scent < Formula
  desc "Recursive byte-oriented grep in wolf with terminal colour"
  homepage "https://github.com/wolffe-lang/scent"
  url "https://github.com/wolffe-lang/scent/archive/refs/tags/v0.2.0.tar.gz"
  sha256 "RELEASE-LANE-FILLS-THIS"
  license "GPL-3.0-or-later"
  depends_on "llvm" => :build

  resource "wolf" do
    on_macos do
      on_arm do
        url "https://github.com/wolffe-lang/wolf-lang/releases/download/v0.2.36/wolf-0.2.36-aarch64-apple-darwin.tar.gz"
        sha256 "b79d55845f349d56789d9d1cb057ee88b5a7128d3b6dd77ca070707cfa4aa632"
      end
    end
    on_linux do
      on_intel do
        url "https://github.com/wolffe-lang/wolf-lang/releases/download/v0.2.36/wolf-0.2.36-x86_64-unknown-linux-gnu.tar.gz"
        sha256 "d383c74c8cd123b9d9dfaa268271d4f004294f85c2b230237d0ef07027d9500d"
      end
    end
  end

  def install
    source = buildpath
    resource("wolf").stage do
      odie "bundled std pin drift" unless (Pathname.pwd/"std/STD-REV").read.strip == "78b9d3cbc41d51db44d18c40b6694403644d1c83"
      ENV["WOLF_STD"] = (Pathname.pwd/"std").to_s
      system "./wolf", "build", "--release", "--deny-warnings", source/"src/scent.lu", "-o", source/"scent"
    end
    bin.install "scent"
    (libexec/"gnubin").install_symlink bin/"scent" => "grep"
    (libexec/"gnubin").install "wrappers/egrep", "wrappers/fgrep"
    doc.install "README.md", "CHANGELOG.md"
  end

  def caveats
    "Optional grep/egrep/fgrep names are in #{libexec}/gnubin. They do not replace the system grep. Use LC_ALL=C until UTF-8 locale support arrives."
  end

  test do
    ENV["LC_ALL"] = "C"
    assert_equal "ab\n", pipe_output("#{bin}/scent -E '^a[ab]$'", "ab\nno\n", 0)
    assert_equal "aa\n", pipe_output("#{bin}/scent -G '\\(a\\)\\1'", "aa\nno\n", 0)
    (testpath/"tree").mkpath
    (testpath/"tree/a.txt").write "hit\n"
    (testpath/"tree/b.dat").write "miss\n"
    assert_equal "hit\n", shell_output("#{bin}/scent -rh --include='*.txt' hit tree")
    assert_equal "\e[01;31m\e[Khit\e[m\e[K\n", pipe_output("#{bin}/scent --color=always hit", "hit\n", 0)
    assert_match "scent #{version}", shell_output("#{bin}/scent --version")
  end
end
