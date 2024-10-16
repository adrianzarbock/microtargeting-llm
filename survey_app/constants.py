import streamlit
from functions import create_list

def topic_dict():
    dict = {0: {"title":"Atomkraft",
                "thesis":"Deutschland soll auch in Zukunft Atomkraft zur Energiegewinnung nutzen.",
                "antithesis":"Deutschland soll in Zukunft auf Atomkraft zur Energiegewinnung verzichten.",
                            },
            1: {"title":"Parteiverbot",
                "thesis":"Ein Verbot extremistischer Parteien kann notwendig sein, um die Demokratie zu schützen.",
                "antithesis":"Ein Verbot extremistischer Parteien ist keine geeignete Maßnahme, um die Demokratie zu schützen.",
                            },
            2: {"title":"Schuldenbremse",
                "thesis":"Deutschland sollte die Schuldenbremse lockern, um mehr Geld in Infrastruktur und Transformationsprozesse zu investieren.",
                "antithesis":"Deutschland sollte die Schuldenbremse einhalten, auch wenn dies zu Einsparungen in Infrastruktur und Transformationsprozessen führt.",
                            },
            3: {"title":"Tempolimit",
                "thesis":"Auf deutschen Autobahnen sollte es ein generelles Tempolimit geben.",
                "antithesis":"Auf deutschen Autobahnen sollte es kein generelles Tempolimit geben.",
                            }
            }
    return dict
    
def context_dict(num_options=9):
    dict = {0: {"title":"Wirtschaftspolitik",
                "text":"Manche wollen weniger Steuern und Abgaben, auch wenn das weniger sozialstaatliche Leistungen bedeutet. Andere wollen mehr sozialstaatliche Leistungen, auch wenn das mehr Steuern und Abgaben bedeutet.\n\n Wie ist Ihre Meinung zu diesem Thema?",
                "options": create_list(num_options,
                                       "Vorrang für weniger Steuern und Abgaben, auch wenn das weniger sozialstaatliche Leistungen bedeutet",
                                       "Neutral",
                                       "Vorrang für mehr sozialstaatliche Leistungen, auch wenn das mehr Steuern und Abgaben bedeutet")
                },
            1: {"title":"Gesellschaftspolitik",
                "text":"Manche sind der Meinung, dass eine freie persönliche Entfaltung und gesellschaftliche Vielfalt höchste Priorität haben sollten, auch wenn dies traditionelle Werte und Strukturen herausfordert. Andere legen größten Wert auf den Erhalt und die Pflege traditioneller Werte und Strukturen, auch wenn dies eine freie persönliche Entfaltung und gesellschaftliche Vielfalt einschränkt.\n\n Wie ist Ihre Meinung zu diesem Thema?",
                "options": create_list(num_options,
                                       "Vorrang für eine freie persönliche Entfaltung und gesellschaftliche Vielfalt, auch wenn es traditionelle Werte und Strukturen in Frage stellt",
                                       "Neutral",
                                       "Vorrang für traditionelle Werte und Strukturen, auch wenn es die eine freie persönliche Entfaltung und gesellschaftliche Vielfalt einschränkt")
                },
            2: {"title":"Klimapolitik",
                "text":"Manche meinen, dass die Bekämpfung des Klimawandels auf jeden Fall Vorrang haben sollte, auch wenn dies auf Kosten des gegenwärtigen Lebensstandards geht. Andere meinen, dass der Erhalt des gegenwärtigen Lebensstandards auf jeden Fall Vorrang haben sollte, auch wenn das die Bekämpfung des Klimawandels erschwert.\n\n Wie ist Ihre Meinung zu diesem Thema?",
                "options": create_list(num_options,
                                        "Vorrang für die Bekämpfung des Klimawandels, auch wenn es auf Kosten des gegenwärtigen Lebensstandards geht",
                                        "Neutral",
                                        "Vorrang für den Erhalt des gegenwärtigen Lebensstandards, auch wenn es die Bekämpfung des Klimawandels erschwert"),
                },
            3: {"title":"Globalisierung",
                "text":"Manche argumentieren, dass nationale Interessen und die nationale Souveränität immer Vorrang haben sollten, auch wenn dies die internationale Zusammenarbeit und globale Solidarität beeinträchtigen könnte. Andere sind der Ansicht, dass globale Solidarität und internationale Zusammenarbeit immer Vorrang haben sollten, selbst wenn dies nationale Interessen und die nationale Souveränität herausfordern könnte.\n\n Wie ist Ihre Meinung zu diesem Thema?",
                "options": create_list(num_options,
                                        "Vorrang für nationale Interessen und Souveränität, auch wenn es die internationale Zusammenarbeit beeinträchtigt",
                                        "Neutral",
                                        "Vorrang für internationale Zusammenarbeit und globale Solidarität, auch wenn es die nationale Souveränität herausfordert"),
                 }
            }
    return dict

def agree_options(num_options=9):
    list = create_list(num_options, "Stimme überhaupt nicht zu", "Neutral", "Stimme voll und ganz zu")
    return list

def binary_options():
    list = ["Stimme (eher) zu", "Stimme (eher) nicht zu"]
    return list