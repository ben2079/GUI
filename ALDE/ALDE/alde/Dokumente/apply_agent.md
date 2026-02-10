 # Build structured prompt following the document specification

 
        job_title = parsed_data.get("job_title", "Position")
        company = parsed_data.get("company", "Ihr Unternehmen")
        contact = parsed_data.get("contact", "")
        current_date = datetime.now().strftime("%d.%m.%Y")
        
        draft_messages = [
            {"role": "system", "content": (
                "You are a professional cover letter writer specializing in IT/Application Development. "
                "Generate a compelling, personalized cover letter in German. "
                "Structure: Briefkopf (Anschrift des Arbeitgebers), Betreff, Anrede, Einleitung, "
                "Hauptteil (USP, relevante Beispiele), Schluss (Call-to-Action), Grußformel. "
                f"Use current date: {current_date}. "
                "Be concise, professional, and enthusiastic."
            )},

            {"role": "user", "content": (
                f"Create a cover letter for this job:\n\n" 
                f"Company: {company}\n"
                f"Position: {job_title}\n" 
                f"Contact: {contact}\n\n"
                f"Applicant Profile:\n{profile}\n\n"
                f"Additional Context:\n{context}\n\n"
                f"Job Posting:\n{posting}"
            )}
        ]