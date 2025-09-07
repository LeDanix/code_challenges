import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";

interface Result {
    first_name: string[];
    last_name: string[];
    chance: number;
}

export default function NameSplitter() {
    const [name, setName] = useState("");
    const [country, setCountry] = useState("");
    const [result, setResult] = useState<Result | null>(null);
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [countries, setCountries] = useState<string[]>([]);
    const inputRef = useRef<HTMLInputElement | null>(null);

    useEffect(() => {
        let mounted = true;
        fetch("http://localhost:8000/get-countries")
            .then((res) => res.json())
            .then((data) => {
                if (!mounted) return;
                if (data?.countries && Array.isArray(data.countries)) {
                    setCountries(data.countries);
                }
            })
            .catch((err) => console.error("Could not load countries:", err));

        return () => { mounted = false; };
    }, []);

    const handleSubmit = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (!name.trim()) return;

        setSubmitted(true);
        setLoading(true);

        try {
            const response = await fetch("http://localhost:8000/parse-name", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ full_name: name, country: country || null }),
            });
            if (!response.ok) throw new Error("Bad response from server");
            const data = await response.json();

            const normalized: Result = {
                first_name: Array.isArray(data.first_name) ? data.first_name : [String(data.first_name || "")],
                last_name: Array.isArray(data.last_name) ? data.last_name : [String(data.last_name || "")],
                chance: typeof data.chance === "number" ? Math.max(0, Math.min(100, Math.round(data.chance))) : 0,
            };

            setResult(normalized);
            inputRef.current?.blur();
        } catch (err) {
            console.error("Error parsing name:", err);
            setResult({ first_name: ["-"], last_name: ["-"], chance: 0 });
        } finally {
            setLoading(false);
        }
    };

    const progressStyle = (chance: number) => ({
        width: `${chance}%`,
        background: "linear-gradient(90deg, #2563eb 0%, #3b82f6 50%, #4ade80 100%)",
    });

    return (
        <div className="min-h-screen w-full flex flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white px-4">
            <motion.div
                initial={{ y: 0 }}
                animate={{ y: result ? -120 : 0 }}
                transition={{ type: "spring", stiffness: 100, damping: 18 }}
                className="w-full max-w-3xl"
            >
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-extrabold text-blue-700 mb-2">What The Name!</h1>
                    <p className="text-gray-600 text-base">
                        Find the name of <span className="text-blue-700 font-semibold">THAT</span> person
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="relative w-full">
                    <div
                        className="w-full rounded-full shadow-lg px-4 py-3 flex items-center gap-3"
                        style={{
                            background: "linear-gradient(90deg, rgba(255,255,255,0.95) 0%, rgba(239,246,255,0.95) 100%)",
                            border: "1px solid rgba(37,99,235,0.12)",
                        }}
                    >
                        <input
                            ref={inputRef}
                            type="text"
                            placeholder={`Enter full name...`}
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="flex-1 bg-transparent placeholder-blue-400 text-gray-800 focus:outline-none text-lg"
                            aria-label="Full name"
                        />

                        {/* Divider */}
                        <div className="h-6 w-px bg-blue-200 mx-3" />

                        {/* Country select inline, separated por divider */}
                        <select
                            value={country}
                            onChange={(e) => setCountry(e.target.value)}
                            className="bg-transparent text-gray-800 text-sm focus:outline-none max-h-12 overflow-y-auto"
                            aria-label="Country"
                        >
                            <option value="">Country</option>
                            {countries.map((c) => (
                                <option key={c} value={c}>{c}</option>
                            ))}
                        </select>

                        <button
                            type="submit"
                            className="ml-2 flex items-center justify-center w-11 h-11 rounded-full shadow-inner"
                            style={{
                                background: "linear-gradient(180deg,#2563eb,#1d4ed8)",
                                boxShadow: "0 6px 18px rgba(37,99,235,0.18)",
                            }}
                            disabled={loading || !name.trim()}
                        >
                            {loading ? (
                                <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="12" cy="12" r="10" stroke="white" strokeWidth="4" strokeOpacity="0.2" />
                                    <path d="M22 12a10 10 0 00-10-10" stroke="white" strokeWidth="4" strokeLinecap="round" />
                                </svg>
                            ) : (
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="w-5 h-5 text-white" fill="none">
                                    <path d="M5 12h14" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    <path d="M12 5l7 7-7 7" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            )}
                        </button>
                    </div>
                </form>

                {result && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.98 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.45 }}
                        className="mx-auto mt-8 w-full max-w-3xl bg-white rounded-2xl shadow-2xl p-6"
                        aria-live="polite"
                    >
                        <h3 className="text-lg font-semibold text-gray-800 mb-4">Result</h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <div className="text-sm text-gray-500">First name</div>
                                <div className="mt-2 flex flex-wrap gap-3">
                                    {result.first_name.map((n, idx) => (
                                        <span key={idx} className="inline-block px-4 py-2 rounded-full text-sm bg-blue-50 text-blue-700">{n}</span>
                                    ))}
                                </div>
                            </div>
                            <div>
                                <div className="text-sm text-gray-500">Last name</div>
                                <div className="mt-2 flex flex-wrap gap-3">
                                    {result.last_name.map((n, idx) => (
                                        <span key={idx} className="inline-block px-4 py-2 rounded-full text-sm bg-blue-50 text-blue-700">{n}</span>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <div className="mt-6">
                            <div className="flex items-center justify-between mb-2">
                                <div className="text-sm text-gray-500">Confidence</div>
                                <div className="text-sm font-medium text-gray-700">{result.chance}%</div>
                            </div>
                            <div className="w-full bg-blue-100 rounded-full h-4 overflow-hidden">
                                <div className="h-4 rounded-full transition-all duration-700" style={progressStyle(result.chance)} />
                            </div>
                        </div>


                        <div className="mt-4 text-sm text-gray-500 flex items-center justify-between">
                            <div>Detected using server model</div>
                            <button
                                className="text-blue-600 hover:underline text-sm"
                                onClick={() => {
                                    setResult(null);
                                    setSubmitted(false);
                                    setName("");
                                    setCountry("");
                                    setTimeout(() => inputRef.current?.focus(), 50);
                                }}
                            >
                                Try again
                            </button>
                        </div>
                    </motion.div>
                )}
            </motion.div>
        </div >
    );
}
